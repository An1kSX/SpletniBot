from aiogram import Router, F
from aiogram.enums import ChatType
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.dispatcher import FSMContext


from app.keyboards.user.builder import build_user_menu_keyboard, build_rules_keyboard
from app.features.user.service import UserService
from app.content import common_rules

from .filter import UserFilter


router = Router(name="user_router")


@router.message(F.chat.type == ChatType.PRIVATE &
                CommandStart() &
                UserFilter()
)
async def handle_start_message(message: Message, state: FSMContext):
    user_id = message.from_user.id
    validation = await UserService.validate_user_access(user_id, state)
    if not validation["access"]:
        if validation["text"]:
            await message.reply(validation["text"], reply_markup=validation["markup"])
        return

    kb = await build_user_menu_keyboard()
    await message.reply("Главное меню", reply_markup=kb)


@router.message(F.chat.type == ChatType.PRIVATE &
                UserFilter()
)
async def handler_private_message(message: Message, state: FSMContext):
    user_id = message.from_user.id
    validation = await UserService.validate_user_access(user_id, state)
    if not validation["access"]:
        if validation["text"]:
            await message.reply(validation["text"], reply_markup=validation["markup"])
        return
    
    text = message.text.lower()
    if text == "правила":
        await message.reply(common_rules)

    elif text == "помощь":
        pass

    elif text == "признание":
        pass

    elif text == "смена никнейма":
        pass