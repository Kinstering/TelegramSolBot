from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton)

main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🔰 Wallet', callback_data='wallet')],
    [InlineKeyboardButton(text='🛒 Buy token', callback_data='buy_token')],
    [InlineKeyboardButton(text='💰 Sell token', callback_data='sell_token')]
])

def button_wallet(public_key):
    wallet = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='🔍 View in Solscan', url=f'https://solscan.io/account/{public_key}')],
        [InlineKeyboardButton(text='💸 Withdraw all SOL', callback_data='withdraw_all_sol'),
         InlineKeyboardButton(text='🔢 Withdraw X SOL', callback_data='withdraw_x_sol')],
        [InlineKeyboardButton(text='🔑 Export Private Key', callback_data='export_private_key')],
        [InlineKeyboardButton(text='🔄 Refresh', callback_data='refresh_wallet'),
         InlineKeyboardButton(text='🏠 Home', callback_data='home')],
    ])
    return wallet