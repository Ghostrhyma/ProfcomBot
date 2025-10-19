import asyncio
from .forapi.app_api import get_data_to_bot_mess
from .forapi.json_funcs import get_last_post_from_group, read_from_json

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

            text, photos = data
            if photos:
                await bot.send_photo(chat_item["chat_id"],message_thread_id=chat_item["message_thread_id"], photo=photos[0]['url'], caption=text)
            else:
                await bot.send_message(chat_item["chat_id"], message_thread_id=chat_item["message_thread_id"], text=text)
        await asyncio.sleep(60)