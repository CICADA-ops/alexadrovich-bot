from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardButton, InlineKeyboardMarkup)

menu_buttons = [
    [KeyboardButton(text='Скачать видео с Youtube')],
    [KeyboardButton(text='Конвертер')],
    [KeyboardButton(text='Расшифровать голосовое')]
]

menu_keyboard = ReplyKeyboardMarkup(keyboard=menu_buttons,
                                    resize_keyboard=True,
                                    input_field_placeholder="Выберите опцию")
