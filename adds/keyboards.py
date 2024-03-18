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

format_buttons = [
    [InlineKeyboardButton(text='png', callback_data='png')],
    [InlineKeyboardButton(text='jpg', callback_data='jpg')],
    [InlineKeyboardButton(text='webp', callback_data='webp')],
]

format_keyboard = InlineKeyboardMarkup(inline_keyboard=format_buttons)
