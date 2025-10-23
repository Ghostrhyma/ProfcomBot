from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from .forapi.json_funcs import add_to_json, delete_chat_from_json, read_from_json
from app.forapi.app_api import get_last_post_from_group
import app.keyboards as kb

from datetime import datetime
import asyncio

import re

router = Router()

class DomainData(StatesGroup):
    domain = State()


@router.message(Command("start"))
async def get_start(message: Message):
    await message.answer("Крч ну это ты там /push_domain")
    # chat_data = {"chat_id": str(message.chat.id), "message_thread_id": message.message_thread_id}
    # await add_to_json("app/forapi/chats.json", chat_data)
    # await message.answer("Подписка на посты Профкома активирована!")


@router.message(Command("stop"))
async def stop_bot_in_chat(message: Message):
    chat_id = str(message.chat.id)
    await delete_chat_from_json("app/forapi/chats.json", "chat_id", chat_id)
    await message.answer("Подписка на посты Профкома деактивирована!")


@router.message(Command("push_domain"))
async def get_domain(message: Message, state: FSMContext):
    await state.set_state(DomainData.domain)
    await message.answer("Введите ссылку на группу, посты которой хотите получать")


@router.message(DomainData.domain)
async def after_get_domain(message: Message, state: FSMContext):
    """
        Пометка на будущее

        Если бот интегрируется с чатом или супергруппой, то боту нужно выдать права администратора

    """
    # -------- Вынести в отдельную функцию --------------
    vk_pattern = "https://vk.com/([^/?#]+)"
    match = re.search(vk_pattern, message.text)
    print("Проверка домена выполнена")
    # ---------------------------------------------------

    if match:
        print("Домен обнаружен")
        await state.update_data(domain=match.group(1))
        data = await state.get_data()


        domain = data["domain"]

        chat_info = {
                "chat_id": message.chat.id,
                "message_thread_id": message.message_thread_id
        }

        global domain_in_file

        print("Отправляем запрос для подтверждения существования группы")
        resp = await get_last_post_from_group(domain=domain)
        
        # Позже разбить код ниже на подфункции

        if isinstance(resp, bool):
            print("Такой группы не существует или у группы отсутствубт посты")
            await message.answer("Такой группы не существует или у группы отсутствубт посты")
        else:
            domains_list = await read_from_json("app/forapi/domains.json")
            
            checkDomainInFile = False
            print("Файл прочитан")
            for domain_item in domains_list:
                if domain == domain_item["domain"]:
                    domain_in_file = domain_item
                    checkDomainInFile = True
            
            print("Проверка домена закончена")
            if not checkDomainInFile:
                
                chats = []
                chats.append(chat_info)

                new_domain = {
                    "domain": domain,
                    "chat": chats
                }

                await add_to_json("app/forapi/domains.json", new_domain)
            else:
                checkChatInDomen = False
                for chat in domain_in_file["chat"]:
                    if chat_info["chat_id"] == chat["chat_id"]:
                        checkChatInDomen = True

                if not checkChatInDomen:
                    await delete_chat_from_json("app/forapi/domains.json", "domain", domain)
                    domain_in_file["chat"].append(chat_info)
                    print(f"Изменены данные для домена {domain}")
                    await add_to_json("app/forapi/domains.json", domain_in_file)
                else:
                    print(f"Нет изменений данных для домена {domain}")

            await message.answer("Ссылка успешно обработана")
            await state.clear()
    else:
        await message.answer("Убедитесь, что предоставленная ссылка корректна")






# Ответы на рандомные сообщения пользователя

@router.message((F.text == "penis") | (F.text == "пенис"))
async def exclipt_ans(message: Message):
    await message.answer("А ты оригинален")

@router.message((F.text == "парадокси") | (F.text == "paradoxy"))
async def exclipt_ans(message: Message):
    await message.answer("Думаю она даже не целоваолась")

@router.message((F.text.lower() == "а ты оригинален"))
async def exclipt_ans(message: Message):
    await message.answer("Пенис")
