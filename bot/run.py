from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
import asyncio, os, logging, sys

from app.handlers import router, get_start

load_dotenv()

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())