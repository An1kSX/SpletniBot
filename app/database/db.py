import asyncio
import asyncpg

from typing import List, Tuple, Dict

from app.core.config import settings
from app.core.logger import ModuleLogger


logger = ModuleLogger(
	module_name=__name__,
	log_level=settings.log_level
).get_logger()


class Database:
	def __init__(self):
		self.host = settings.postgres_host
		self.port = settings.postgres_port
		self.user = settings.postgres_user
		self.password = settings.postgres_password
		self.dbname = settings.postgres_db

		missing = [n for n, v in [
			("POSTGRES_HOST", self.host),
			("POSTGRES_USER", self.user),
			("POSTGRES_DB", self.dbname),
		] if not v]

		if missing:
			raise ValueError(f"Missing required env vars: {', '.join(missing)}")

		self.pool: asyncpg.Pool | None = None

	async def connect(self) -> None:
		if self.pool is not None:
			return

		self.pool = await asyncpg.create_pool(
			host=self.host,
			port=self.port,
			user=self.user,
			password=self.password or None,
			database=self.dbname,
			min_size=1,
			max_size=10,
			command_timeout=10,
			timeout=10,
		)

		logger.info("PostgreSQL pool created")

	async def close(self) -> None:
		if self.pool is not None:
			await self.pool.close()
			self.pool = None
			logger.info("PostgreSQL pool closed")

	async def __aenter__(self):
		await self.connect()
		return self

	async def __aexit__(self, exc_type, exc_value, traceback):
		await self.close()

	async def execute_query(self, query: str, params: Tuple = ()) -> Dict | List[Dict]:
		if self.pool is None:
			await self.connect()

		try:
			logger.info("Executing query: %s", query)

			async with self.pool.acquire() as conn:
				stmt = await conn.prepare(query)

				if stmt.get_attributes():
					rows = await conn.fetch(query, *params)
					return [dict(row) for row in rows]

				result = await conn.execute(query, *params)

				return {
					"status": result
				}

		except asyncpg.UniqueViolationError as e:
			logger.error("UniqueViolationError: %s | query=%s | params=%s", e, query, params)
			raise

		except asyncpg.ForeignKeyViolationError as e:
			logger.error("ForeignKeyViolationError: %s | query=%s | params=%s", e, query, params)
			raise

		except asyncio.TimeoutError as e:
			logger.error("Database timeout: %s | query=%s", e, query)
			raise

		except Exception as e:
			logger.error("PostgreSQL error: %s | query=%s | params=%s", e, query, params)
			raise

	async def execute_many(self, query: str, params: List[Tuple]) -> Dict:
		if self.pool is None:
			await self.connect()

		try:
			logger.info("Executing many: %s | params count: %s", query, len(params))

			async with self.pool.acquire() as conn:
				async with conn.transaction():
					await conn.executemany(query, params)

			return {
				"rowcount": len(params)
			}

		except asyncpg.UniqueViolationError as e:
			logger.error("UniqueViolationError: %s | query=%s", e, query)
			raise

		except asyncpg.ForeignKeyViolationError as e:
			logger.error("ForeignKeyViolationError: %s | query=%s", e, query)
			raise

		except asyncio.TimeoutError as e:
			logger.error("Database timeout: %s | query=%s", e, query)
			raise

		except Exception as e:
			logger.error("PostgreSQL error: %s | query=%s", e, query)
			raise

	async def execute_script(self, script: str) -> None:
		if self.pool is None:
			await self.connect()

		try:
			logger.info("Executing SQL script")

			async with self.pool.acquire() as conn:
				await conn.execute(script)

		except asyncio.TimeoutError as e:
			logger.error("Database script timeout: %s", e)
			raise

		except Exception as e:
			logger.error("PostgreSQL script error: %s", e)
			raise


database = Database()
