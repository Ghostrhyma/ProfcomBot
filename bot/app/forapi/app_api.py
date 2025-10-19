from .json_funcs import get_last_post_from_json

import aiohttp
import requests
from dotenv import load_dotenv
import os

load_dotenv()

async def get_last_post_from_group():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.vk.com/method/wall.get", params={
            "access_token": os.getenv("TOKEN"),
            "v": os.getenv("VERSION"),
            "domain": os.getenv("DOMAIN"),
            "count": 1
        }) as response:
            data = await response.json()
            return data["response"]["items"][0]



async def get_data_to_bot_mess(chat_id, last_post):
    from_json = await get_last_post_from_json(f"app/forapi/posts_dir/{chat_id}_posts.json", last_post)
    data, flag = from_json[0], from_json[1]
    if flag:
        try:
            copy_data = data["copy_history"]

            text = copy_data[0]["text"]
            photos = []

            for item in copy_data[0].get("attachments", []):
                if item.get("type") == "photo":
                    for photo in item["photo"]["sizes"]:
                        if photo["type"] == 'x':
                            photos.append(photo)

            return (text, photos)

        except KeyError:
            not_copy_data = data

            text = not_copy_data["text"]
            photos = []

            for item in not_copy_data["attachments"]:
                if item.get("type") == "photo":
                    for photo in item["photo"]["sizes"]:
                        if photo["type"] == 'x':
                            photos.append(photo)

            return (text, photos)
    else:
        return flag


# if __name__ == "__main__":
#     data = get_data_to_bot_mess()
#     print(data[0], data[1])
