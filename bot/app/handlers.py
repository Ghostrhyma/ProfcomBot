from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from .forapi.json_funcs import add_to_json

from datetime import datetime
import asyncio

router = Router()


@router.message(CommandStart)
async def get_start(message: Message):
    chat_data = {"chat_id": str(message.chat.id), "message_thread_id": message.message_thread_id}
    await add_to_json("app/forapi/chats.json", chat_data)
    await message.answer("Подписка на посты Профкома активирована!")