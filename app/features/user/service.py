from aiogram import Bot
from aiogram.enums import ChatMemberStatus
from aiogram.types import User
from typing import List, Dict, Optional

from app.core.config import settings
from app.core.logger import ModuleLogger

from app.database import database


logger = ModuleLogger(
	module_name=__name__,
	log_level=settings.log_level
	).get_logger()


class UserService:
	@staticmethod
	async def is_subscriber(
		bot: Bot,
		user_id: int
	) -> bool:
		try:
			member = await bot.get_chat_member(
					chat_id=settings.spletni_channel_id,
					user_id=user_id
				)

			return member.status not in (
					ChatMemberStatus.KICKED,
					ChatMemberStatus.LEFT
				)

		except Exception as e:
			logger.exception(f"Ошибка при проверке подписки пользователя на канал: {e}")
			raise

	@staticmethod
	async def is_banned(
		user_id: int
	) -> bool:
		try:
			query = "SELECT 1 FROM banned WHERE user_id = %s"
			params = (user_id, )

			result = await database.execute_query(query, params)

			return bool(result)

		except Exception as e:
			logger.exception(f"Ошибка проверки забанен ли пользователь: {e}")
			raise

	@staticmethod
	async def has_accepted_rules(
		user_id: int
	) -> bool:
		try:
			query = """
				SELECT 1
				FROM users
				WHERE
					telegram_id = %s AND
					accepted_rules IS TRUE
			"""
			params = (user_id, )

			result = await database.execute_query(query, params)

			return bool(result)

		except Exception as e:
			logger.exception(f"Ошибка при проверке принятия правил пользователем: {e}")
			raise

	@staticmethod
	async def accept_rules(
		user_id: int
	) -> Dict:
		try:
			query = """
				UPDATE users
				SET
					accepted_rules = true
				WHERE
					telegram_id = %s
			"""
			params = (user_id, )

			result = await database.execute_query(query, params)

			return result

		except Exception as e:
			logger.exception(f"Ошибка при принятии правил пользователем: {e}")
			raise

	@staticmethod
	async def sync_user(
		user: User
	):
		try:
			query = """
				INSERT INTO users (
					telegram_id,
					nickname,
					username,
					first_name,
					last_name,
					role_id
				)
				VALUES (
					%s,
					%s,
					%s,
					%s,
					%s,
					(SELECT id FROM roles WHERE title = %s)
				)
				ON CONFLICT (telegram_id) DO UPDATE SET
					username = EXCLUDED.username,
					first_name = EXCLUDED.first_name,
					last_name = EXCLUDED.last_name
			"""
			params = (
				user.id,
				None,
				user.username,
				user.first_name,
				user.last_name,
				'user'
			)

			return await database.execute_query(query, params)

		except Exception as e:
			logger.exception(f"Ошибка синхронизации пользователя: {e}")
			raise
