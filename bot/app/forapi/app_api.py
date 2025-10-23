from .json_funcs import get_last_post_from_json

import aiohttp
import requests
from dotenv import load_dotenv
import os
import ssl, certifi
load_dotenv()

ssl_context = ssl.create_default_context(cafile=certifi.where())


async def get_last_post_from_group(domain: str):
    try:
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context)) as session:
            async with session.get("https://api.vk.com/method/wall.get", params={
                "access_token": str(os.getenv("TOKEN")),
                "v": os.getenv("VERSION"),
                # "domain": str(os.getenv("DOMAIN")),
                "domain": domain,
                "count": 1
            }) as response:
                data = await response.json()
                return data["response"]["items"][0]
    except KeyError:
        return False



async def get_data_to_bot_mess(domain, last_post):
    from_json = await get_last_post_from_json(f"app/forapi/posts_dir/{domain}_posts.json", last_post)
    data, flag = from_json[0], from_json[1]
    if flag:
        try:
            copy_data = data["copy_history"]

            text = copy_data[0]["text"]

            if text == "":
                text = "."

            photos = []
            files = []
            videos = []

            for item in copy_data[0].get("attachments", []):
                if item.get("type") == "photo":
                    for photo in item["photo"]["sizes"]:
                        if photo["type"] == 'x':
                            photos.append(photo)
                if item.get("type") == "doc":
                    files.append(item["doc"])
                if item.get("type") == "video":
                    owner_id = item["video"]["owner_id"]
                    video_id = item["video"]["id"]
                    preview = item["video"]["image"][3]["url"]
                    try:
                        access_key = item["video"]["access_key"]
                        link_for_video = f"https://vk.com/video{owner_id}_{video_id}?access_key={access_key}"

                        video = {
                            "url": link_for_video,
                            "preview": preview
                        }
                        videos.append(video)
                    except KeyError:
                        link_for_video = f"https://vk.com/video{owner_id}_{video_id}"

                        video = {
                            "url": link_for_video,
                            "preview": preview
                        }

                        videos.append(video)

            return (text, photos, files, videos)

        except KeyError:
            not_copy_data = data

            text = not_copy_data["text"]
            if text == "":
                text = "."

            photos = []
            files = []
            videos = []

            for item in not_copy_data["attachments"]:
                if item.get("type") == "photo":
                    for photo in item["photo"]["sizes"]:
                        if photo["type"] == 'x':
                            photos.append(photo)
                if item.get("type") == "doc":
                    files.append(item["doc"])
                if item.get("type") == "video":
                    owner_id = item["video"]["owner_id"]
                    video_id = item["video"]["id"]
                    preview = item["video"]["image"][3]["url"]
                    
                    try:
                        access_key = item["video"]["access_key"]
                        link_for_video = f"https://vk.com/video{owner_id}_{video_id}?access_key={access_key}"

                        video = {
                            "url": link_for_video,
                            "preview": preview
                        }

                        videos.append(video)
                    except KeyError:
                        link_for_video = f"https://vk.com/video{owner_id}_{video_id}"

                        video = {
                            "url": link_for_video,
                            "preview": preview
                        }

                        videos.append(video)

            return (text, photos, files, videos)
    else:
        return flag


# if __name__ == "__main__":
#     data = get_data_to_bot_mess()
#     print(data[0], data[1])
