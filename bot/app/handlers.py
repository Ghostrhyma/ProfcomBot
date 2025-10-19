from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from .forapi.app_api import get_data_to_bot_mess
from .forapi.json_funcs import get_last_post_from_group, read_from_json, add_to_json

from datetime import datetime
import asyncio

router = Router()


@router.message(CommandStart)
async def get_start(message: Message):
    chat_data = {"chat_id": str(message.chat.id), "date": str(datetime.now())}
    await add_to_json("app/forapi/chats.json", chat_data)
    await message.answer("Подписка на посты Профкома активирована!")