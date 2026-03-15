from aiogram.utils import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup



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
		logger.exception(f"Ошибка построения клавиатуры пользователя: {e}")
		raise