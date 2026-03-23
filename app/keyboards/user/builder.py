from aiogram.utils import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup

from app.core.logger import ModuleLogger

logger = ModuleLogger(
	module_name=__name__,
).get_logger()


async def build_user_menu_keyboard() -> ReplyKeyboardMarkup:
	try:
		kb = ReplyKeyboardBuilder()

		kb.button(
			text="Помощь",
			icon_custom_emoji_id=5470092785094765546
		)
		kb.button(
			text="Признание",
			icon_custom_emoji_id=5471921818392600919
		)
		kb.button(
			text="Правила",
			icon_custom_emoji_id=5472410705929971383
		)
		kb.button(
			text="Смена никнейма",
			icon_custom_emoji_id=5472033358693280429
		)
		kb.adjust(2)

		return kb.as_markup(resize_keyboard=True)

	except Exception as e:
		logger.exception(f"Ошибка построения клавиатуры пользователя")
		raise

async def build_rules_keyboard() -> InlineKeyboardMarkup:
	try:
		kb = InlineKeyboardBuilder()

		kb.button(
			text="Принять",
			icon_custom_emoji_id=5472248313216510573
		)
		kb.button(
			text="Отклонить",
			icon_custom_emoji_id=5472248313216510573
		)
		kb.adjust(2)

		return kb.as_markup(resize_keyboard=True)

	except Exception as e:
		logger.exception(f"Ошибка построения клавиатуры правил")
		raise

async def build_cancel_keyboard() -> ReplyKeyboardMarkup:
	try:
		kb = ReplyKeyboardBuilder()

		kb.button(
			text="Отмена",
			icon_custom_emoji_id=5335051484230854758
		)

		return kb.as_markup(resize_keyboard=True)

	except Exception as e:
		logger.exception(f"Ошибка построения клавиатуры отмены")
		raise

async def build_change_nickname_keyboard() -> ReplyKeyboardMarkup:
	try:
		kb = ReplyKeyboardBuilder()

		kb.button(
			text="Удалить никнейм",
			icon_custom_emoji_id=5445267414562389170
		)

		kb.button(
			text="Отмена",
			icon_custom_emoji_id=5335051484230854758
		)

		return kb.as_markup(resize_keyboard=True)

	except Exception as e:
		logger.exception(f"Ошибка построения клавиатуры смены никнейма")
		raise