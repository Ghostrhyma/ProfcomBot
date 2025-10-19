import asyncio
from .forapi.app_api import get_data_to_bot_mess
from .forapi.json_funcs import get_last_post_from_group, read_from_json

from aiogram.types import URLInputFile

active_chats = set()


async def background_post_checker(bot):
    """Фоновая проверка новых постов"""
    while True:
        last_post = get_last_post_from_group()
        active_chats = await read_from_json("app/forapi/chats.json")
        for chat_item in active_chats:
            data = await get_data_to_bot_mess(chat_item["chat_id"], last_post)
            if not isinstance(data, tuple):
                continue

            text, photos, files = data
            if photos:
                if files:
                    await bot.send_photo(chat_item["chat_id"], message_thread_id=chat_item["message_thread_id"], photo=photos[0]['url'], caption=text)
                    await bot.send_message(chat_item["chat_id"], text="Файлы к новости выше ⬆️⬆️⬆️", message_thread_id=chat_item["message_thread_id"])
                    for file in files:
                        try:
                            await bot.send_document(chat_item["chat_id"], document=file["url"], message_thread_id=chat_item["message_thread_id"])
                        except Exception as e:
                            await bot.send_message(chat_item["chat_id"], text=file["url"], message_thread_id=chat_item["message_thread_id"])
                else:
                    await bot.send_photo(chat_item["chat_id"],message_thread_id=chat_item["message_thread_id"], photo=photos[0]['url'], caption=text)
            else:
                if files:
                    await bot.send_message(chat_item["chat_id"], text="Файлы к новости выше ⬆️⬆️⬆️", message_thread_id=chat_item["message_thread_id"])
                    for file in files:
                        try:
                            await bot.send_document(chat_item["chat_id"], document=file["url"], message_thread_id=chat_item["message_thread_id"])
                        except Exception as e:
                            await bot.send_message(chat_item["chat_id"], text=file["url"], message_thread_id=chat_item["message_thread_id"])
                else:
                    await bot.send_message(chat_item["chat_id"], message_thread_id=chat_item["message_thread_id"], text=text)

        await asyncio.sleep(60)