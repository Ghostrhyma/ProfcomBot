import asyncio
from .forapi.app_api import get_data_to_bot_mess, get_last_post_from_group
from .forapi.json_funcs import read_from_json

from aiogram.types import InputMediaPhoto
from aiogram import F
from aiogram.types import InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

import app.keyboards as kb
from app.handlers import router


async def get_media_group(photos: list, text: str):
    media = []
    for photo in photos:
        media.append(InputMediaPhoto(media=photo["url"], caption=text))
    return media


async def files_keyboard(files: list, videos: list):
    keyboard = InlineKeyboardBuilder()
    for file in files:
        keyboard.add(InlineKeyboardButton(url=file["url"], text=f"Файл из поста - {file['title']}"))
    for video in videos:
        keyboard.add(InlineKeyboardButton(url=video["url"], text=f"Видео из поста"))
    return keyboard.adjust(2).as_markup()



async def background_post_checker(bot):
    """Фоновая проверка новых постов"""
    while True:
        active_domains = await read_from_json("app/forapi/domains.json")
        for domain_item in active_domains:
            this_domain = domain_item["domain"]
            last_post = await get_last_post_from_group(this_domain)
            await asyncio.sleep(0.5)

            data = await get_data_to_bot_mess(this_domain, last_post)

            if not isinstance(data, tuple):
                continue
            
            # Добавить клавиатуру для перехода на видео
            # Возможно замена получения файлов через inline клавиатуру
            
            for chat_item in domain_item["chat"]:
                text, photos, files, videos = data
                if photos:
                    if len(photos) > 1:
                        media = await get_media_group(photos=photos, text=text)
                        await bot.send_media_group(chat_item["chat_id"], message_thread_id=chat_item["message_thread_id"], media=media)

                        await bot.send_message(
                            chat_item["chat_id"], 
                            message_thread_id=chat_item["message_thread_id"], 
                            text=text,
                            reply_markup=await files_keyboard(files, videos))
                        
                    else:
                        await bot.send_photo(photo=photos[0]["url"], 
                                             caption=text,
                                             chat_id=chat_item["chat_id"],
                                             message_thread_id=chat_item["message_thread_id"],
                                             reply_markup=await files_keyboard(files, videos)
                                             )
                else:
                    if videos:
                        await bot.send_photo(
                            chat_item["chat_id"], 
                            message_thread_id=chat_item["message_thread_id"], 
                            photo=videos[0]["preview"],
                            caption=text,
                            reply_markup=await files_keyboard(files, videos))
                    else:
                        await bot.send_message(
                            chat_item["chat_id"], 
                            message_thread_id=chat_item["message_thread_id"],
                            text=text,
                            reply_markup=await files_keyboard(files, videos))

        await asyncio.sleep(60)