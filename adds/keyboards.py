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

downloading_type_buttons = [
    [InlineKeyboardButton(text='Видео', callback_data='video')],
    [InlineKeyboardButton(text='Аудио', callback_data='audio')],
]

downloading_type_keyboard = InlineKeyboardMarkup(inline_keyboard=downloading_type_buttons)
