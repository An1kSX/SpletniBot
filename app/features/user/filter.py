from aiogram.filters import Filter
from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from .service import UserService


class UserFilter(Filter):
    async def __call__(self, message: Message, state: FSMContext) -> bool:
        user_id = message.from_user.id
        role = await UserService.get_user_role(user_id, state)
        if role == "user":
            return True
        
        return False