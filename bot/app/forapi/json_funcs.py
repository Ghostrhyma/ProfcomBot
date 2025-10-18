import json
import os
import requests
from dotenv import load_dotenv


load_dotenv()

def get_last_post_from_group():
    response = requests.get("https://api.vk.ru/method/wall.get",params={
        "access_token": os.getenv("TOKEN"),
        "v": os.getenv("VERSION"),
        "domain": os.getenv("DOMAIN"),
        "count": 1
    })

    return response.json()["response"]["items"][0]


def read_from_json(filename: str) -> list:
    try:
        with open(filename, "r", encoding="utf-8") as r_json:
            data = json.load(r_json)
            # print(data)
            return data
    except Exception as e:
        print(f"Ошибка: {e}")
        return []


def write_in_json(filename: str, data):
    try:
        with open(filename, "w", encoding="utf-8") as w_json:
            json.dump(data, w_json, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Ошибка: {e}")


def get_last_post_from_json(filename):
    from_file = read_from_json(filename=filename)
    last_data = get_last_post_from_group()
    flag = False
    if from_file[-1] == last_data:
        return (from_file[-1], flag)
    else:
        add_to_json("C:/Projects/VK_API_ProvCom/bot/app/forapi/posts.json", last_data)
        flag = True
        return (last_data, flag) 


def add_to_json(filename: str, data: dict):
    try:
        if os.path.getsize(filename) != 0:
            from_file_data = read_from_json(filename)
            if data not in from_file_data:
                from_file_data.append(data)
            
            write_in_json(filename, from_file_data)
        else:
            new_data = []
            new_data.append(data)
            write_in_json(filename, new_data)
    except Exception as e:
        print(f"Ошибка: {e}")         