from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton)

main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Profile', callback_data='profile')],
    [InlineKeyboardButton(text='Buy token', callback_data='buy_token')],
    [InlineKeyboardButton(text='Sell token', callback_data='sell_token')]
])