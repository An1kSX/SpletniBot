try:
    import uvloop
    uvloop.install()
except:
    pass

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
import asyncio

from app.core.config import settings


async def main() -> None:
    storage = RedisStorage.from_url(settings.redis_dsn)

    dp = Dispatcher(storage=storage)

    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())