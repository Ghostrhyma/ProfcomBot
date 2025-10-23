from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

post_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Файлы поста", callback_data="files"), 
     InlineKeyboardButton(text="Видеофайлы поста", callback_data="videos")]
])
