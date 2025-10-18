from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from .forapi.app_api import get_data_to_bot_mess, get_last_post_from_group

import asyncio

router = Router()



@router.message(CommandStart)
async def get_start(message: Message):
    while(True):
        data = get_data_to_bot_mess()
        if isinstance(data, bool):
            print("Skip")
            await asyncio.sleep(60)
        else:
            text, photos = data
            if len(photos) != 0:
                await message.answer_photo(photo=f"{photos[0]['url']}",caption=f"{text}")
            else:
                await message.answer(f"{text}")