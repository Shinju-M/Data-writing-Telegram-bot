import asyncio
from aiogram import Bot, Dispatcher
import config as cfg
import handlers


bot = Bot()


async def main():
    dp = Dispatcher()

    dp.include_router(handlers.router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())