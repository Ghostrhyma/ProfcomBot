from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

from .forapi.json_funcs import add_to_json, delete_chat_from_json

from datetime import datetime
import asyncio

router = Router()


@router.message(Command("start"))
async def get_start(message: Message):
    chat_data = {"chat_id": str(message.chat.id), "message_thread_id": message.message_thread_id}
    await add_to_json("app/forapi/chats.json", chat_data)
    await message.answer("Подписка на посты Профкома активирована!")

@router.message(Command("stop"))
async def stop_bot_in_chat(message: Message):
    chat_id = str(message.chat.id)
    await delete_chat_from_json("app/forapi/chats.json", "chat_id", chat_id)
    await message.answer("Подписка на посты Профкома деактивирована!")