from aiogram import Router, F
from aiogram.enums import ChatType
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.dispatcher import FSMContext


from app.keyboards.user.builder import build_user_menu_keyboard, build_cancel_keyboard
from app.keyboards.user.builder import build_change_nickname_keyboard
from app.features.user.service import UserService
from app.content import common_rules, help_text, recognition_text, change_nickname_text

from .filter import UserFilter
from .schemas import MenuOption, UserState


router = Router(name="user_router")


@router.message(
    F.chat.type == ChatType.PRIVATE &
    CommandStart() &
    UserFilter()
)
async def handle_start_message(message: Message, state: FSMContext):
    validation = await UserService.validate_user_access(message, state)
    if not validation.access:
        if validation.text:
            await message.reply(validation.text, reply_markup=validation.markup)
        return

    markup = await build_user_menu_keyboard()
    await message.reply("Главное меню", reply_markup=markup)
    await UserService.sync_user(message.from_user)


@router.message(
    F.chat.type == ChatType.PRIVATE &
    UserFilter()
)
async def handler_private_message(message: Message, state: FSMContext):
    validation = await UserService.validate_user_access(message, state)
    if not validation.access:
        if validation.text:
            await message.reply(validation.text, reply_markup=validation.markup)
        return
    
    text = message.text
    if MenuOption.RULES.equals(text):
        await message.reply(common_rules)

    elif MenuOption.HELP.equals(text):
        await state.set_state(UserState.help)
        markup = await build_cancel_keyboard()
        await message.reply(help_text, reply_markup=markup)

    elif MenuOption.RECOGNITION.equals(text):
        await state.set_state(UserState.recognition)
        markup = await build_cancel_keyboard()
        await message.reply(recognition_text, reply_markup=markup)

    elif MenuOption.CHANGE_NICKNAME.equals(text):
        await state.set_state(UserState.change_nickname)
        markup = await build_change_nickname_keyboard()
        nickname = await UserService.get_user_nickname(message.from_user.id, state)
        await message.reply(
            text=change_nickname_text.format(nickname=nickname or "Обыная нумерация"),
            reply_markup=markup
        )

    await UserService.sync_user(message.from_user)


@router.message(
    UserState.help &
    F.chat.type == ChatType.PRIVATE &
    UserFilter()
)
async def handle_help_message(message: Message, state: FSMContext):
    pass


@router.message(
    UserState.recognition &
    F.chat.type == ChatType.PRIVATE &
    UserFilter()
)
async def handle_recognition_message(message: Message, state: FSMContext):
    pass


@router.message(
    UserState.change_nickname &
    F.chat.type == ChatType.PRIVATE &
    UserFilter()
)
async def handle_change_nickname_message(message: Message, state: FSMContext):
    pass