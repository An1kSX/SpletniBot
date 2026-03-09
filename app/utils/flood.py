import time
from hashlib import md5
from redis.asyncio import Redis

from app.core.config import settings


class FloodDetector:
	def __init__(
		self,
		window_seconds: int = 7,
		max_messages: int = 3,
		duplicate_ttl: int = 15,
		duplicate_limit: int = 3,
	):
		self.redis = Redis.from_url(settings.redis_dsn)
		self.window_seconds = window_seconds
		self.max_messages = max_messages
		self.duplicate_ttl = duplicate_ttl
		self.duplicate_limit = duplicate_limit

	async def is_flood(self, user_id: int, message_text: str) -> bool:
		if not message_text:
			message_text = ""

		now = int(time.time())
		window_start = now - self.window_seconds

		rate_key = f"flood:rate:{user_id}"
		duplicate_key = f"flood:duplicate:{user_id}"

		normalized_text = self._normalize_text(message_text)
		text_hash = md5(normalized_text.encode("utf-8")).hexdigest()

		async with self.redis.pipeline(transaction=True) as pipe:
			member = f"{now}:{time.time_ns()}"

			pipe.zadd(rate_key, {member: now})
			pipe.zremrangebyscore(rate_key, 0, window_start)
			pipe.zcard(rate_key)
			pipe.expire(rate_key, self.window_seconds + 2)

			pipe.hgetall(duplicate_key)

			result = await pipe.execute()

		message_count = result[2]
		last_data = result[4]

		if isinstance(last_data, dict):
			last_hash = self._decode(last_data.get(b"hash") or last_data.get("hash"))
			last_count_raw = self._decode(last_data.get(b"count") or last_data.get("count"))
			last_count = int(last_count_raw) if last_count_raw else 0
		else:
			last_hash = None
			last_count = 0

		if last_hash == text_hash:
			new_count = last_count + 1
		else:
			new_count = 1

		await self.redis.hset(
			duplicate_key,
			mapping={
				"hash": text_hash,
				"count": new_count,
			}
		)
		await self.redis.expire(duplicate_key, self.duplicate_ttl)

		if message_count > self.max_messages:
			return True

		if new_count >= self.duplicate_limit:
			return True

		return False

	@staticmethod
	def _normalize_text(text: str) -> str:
		return " ".join(text.strip().lower().split())

	@staticmethod
	def _decode(value):
		if isinstance(value, bytes):
			return value.decode("utf-8")
		return value


flood_detector = FloodDetector()
