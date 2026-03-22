from aiogram import Bot
from aiogram.enums import ChatMemberStatus
from aiogram.types import User, Message
from aiogram.dispatcher import FSMContext
from typing import List, Dict, Optional

from app.core.config import settings
from app.core.logger import ModuleLogger
from app.database import database
from app.keyboards.user.builder import build_rules_keyboard
from app.content import common_rules


logger = ModuleLogger(
	module_name=__name__,
	log_level=settings.log_level
	).get_logger()


class UserService:
	@staticmethod
	async def get_user_role_db(
		user_id: int
	) -> str:
		query = """
			SELECT r.title
			FROM users u
			JOIN roles r ON u.role_id = r.id
			WHERE u.telegram_id = %s
		"""
		params = (user_id, )

		result = await database.execute_query(query, params)

		return result[0]['title']
	
	@staticmethod
	async def get_user_role(
		user_id: int,
		state: FSMContext
	) -> str:
		try:
			data = await state.get_data()
			role = data.get('role')
			if role is not None:
				return role
			
			role = await UserService.get_user_role_db(user_id)
			await state.update_data(role=role)

			return role

		except Exception as e:
			logger.exception(f"Ошибка при получении роли пользователя: {e}")
			raise

	@staticmethod
	async def is_subscriber(
		bot: Bot,
		user_id: int,
		state: FSMContext
	) -> bool:
		try:
			data = await state.get_data()
			is_subscriber = data.get('is_subscriber')
			if is_subscriber is not None:
				return is_subscriber
			
			is_subscriber = await UserService.is_subscriber_api(bot, user_id)
			await state.update_data(is_subscriber=is_subscriber)

		except Exception as e:
			logger.exception(f"Ошибка при проверке подписки пользователя на канал: {e}")
			raise

	@staticmethod
	async def is_subscriber_api(
		bot: Bot,
		user_id: int
	) -> bool:
		member = await bot.get_chat_member(
				chat_id=settings.spletni_channel_id,
				user_id=user_id
			)

		return member.status not in (
				ChatMemberStatus.KICKED,
				ChatMemberStatus.LEFT
			)

	@staticmethod
	async def is_banned(
			user_id: int,
			state: FSMContext
	) -> bool:
		try:
			data = await state.get_data()
			is_banned = data.get('is_banned')
			if is_banned is not None:
				return is_banned
			
			is_banned = await UserService.is_banned_db(user_id)
			await state.update_data(is_banned=is_banned)

		except Exception as e:
			logger.exception(f"Ошибка при проверке забанен ли пользователь: {e}")
			raise

	@staticmethod
	async def is_banned_db(
		user_id: int
	) -> bool:
		query = "SELECT 1 FROM banned WHERE user_id = %s"
		params = (user_id, )

		result = await database.execute_query(query, params)

		return bool(result)


	@staticmethod
	async def has_accepted_rules(
		user_id: int,
		state: FSMContext
	) -> bool:
		try:
			data = await state.get_data()
			accepted_rules = data.get('accepted_rules')
			if accepted_rules is not None:
				return accepted_rules
			
			accepted_rules = await UserService.has_accepted_rules_db(user_id)
			await state.update_data(accepted_rules=accepted_rules)

		except Exception as e:
			logger.exception(f"Ошибка при проверке принятия правил пользователем: {e}")
			raise

	@staticmethod
	async def has_accepted_rules_db(
		user_id: int
	) -> bool:
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

	@staticmethod
	async def accept_rules(
		user_id: int,
		state: FSMContext
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
			await state.update_data(accepted_rules=True)

			return result

		except Exception as e:
			logger.exception(f"Ошибка при принятии правил пользователем: {e}")
			raise

	@staticmethod
	async def sync_user(
		user: User
	) -> Dict:
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

	@staticmethod
	async def validate_user_access(
		user_id: int,
		state: FSMContext
	) -> Dict:
		is_banned = await UserService.is_banned(user_id, state=state)
		if is_banned:
			return {
				"access": False,
				"text": "",
				"markup": None
			}

		is_accepted_rules = await UserService.has_accepted_rules(user_id, state=state)
		if not is_accepted_rules:
			kb = await build_rules_keyboard()
			text = f"Пожалуйста, примите правила, чтобы продолжить.\n\n{common_rules}"
			return {
				"access": False,
				"text": text,
				"markup": kb
			}

		is_subscriber = await UserService.is_subscriber(message.bot, user_id, state=state)
		if not is_subscriber:
			await message.reply("Пожалуйста, подпишитесь на наш канал, чтобы использовать бота.")
			return {
				"access": False,
				"text": "Пожалуйста, подпишитесь на наш канал, чтобы использовать бота.",
				"markup": None
			}
