from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
import asyncio, os, logging, sys

from app.handlers import router

from app.background_task import background_post_checker


load_dotenv()

bot = Bot(token=str(os.getenv("BOT_TOKEN")))
dp = Dispatcher()
dp.include_router(router)

async def on_startup(bot):
    # Запуск фоновой задачи
    asyncio.create_task(background_post_checker(bot))
    print("-- Фоновая задача запущена вместе с ботом")

async def main():
    await on_startup(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())