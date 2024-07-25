from aiogram import Bot, Dispatcher, F, types, Router
from aiogram.types import Message, CallbackQuery, ContentType
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from aiogram.enums.chat_member_status import ChatMemberStatus
from aiogram.filters import CommandStart, Command
import aiogram.exceptions as exceptions

import app.keyboard as kb
from app.db import Database
from config import TOKEN
import app.solana as sol
import app.func as func

user_handlers = Router()
bot = Bot(token=TOKEN)
db = Database('database.db')

class userStates(StatesGroup):
    top_up = State()

# REGISTER
@user_handlers.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    user_id = message.from_user.id
    welcome_message = (
        '🎉 Welcome to the Fan Token Purchase Bot! 🎉\n\n'
        '🚀 This bot allows you to purchase fan tokens on the Solana network.\n'
        '🔐 A new Solana wallet will be created for you to manage your tokens.\n\n'
        '📌 Your public key will be displayed once your wallet is created.\n'
        '💡 If you have any questions or need assistance, feel free to ask!\n'
        '\n'
        'Get started by exploring the options below:'
    )

    if not db.user_exists(user_id):
        public_key, private_key = sol.create_wallet()
        db.add_user(user_id, private_key, public_key)
        welcome_message += f'\n\n🆕 Your new Solana wallet has been created!\n🔑 Public Key: `{public_key}`'

    await message.answer(welcome_message, parse_mode='Markdown', reply_markup=kb.main)

# ------------------ PROFILE ---------------------

@user_handlers.callback_query(F.data == 'wallet')
async def cmd_profile(callback: CallbackQuery):
    user_id = callback.from_user.id
    if db.user_exists(user_id):
        public_key = db.get_public_key(user_id)
        sol_balance = await func.get_sol_balance(public_key)
        profile_message = (
            f'🔑 *Your Solana Wallet Profile*\n\n'
            f'🌟 *Address*: `{public_key}`\n'
            f'💵 *Balance:* `{sol_balance}` SOL\n'
            f'💼 Tap to copy the address and send SOL to deposit.\n'
        )
    else:
        profile_message = (
            '❌ **No wallet found!**\n\n'
            'It looks like you haven\'t created a wallet yet.\n'
            '🔄 Please start by creating a new wallet to begin purchasing fan tokens.'
        )

    await callback.message.edit_text(profile_message, parse_mode='Markdown', reply_markup=kb.button_wallet(public_key))

# ---------------- BUY SOL -------------------

@user_handlers.callback_query(F.data == 'buy_token')
async def cmd_profile(callback: CallbackQuery):
    pass

@user_handlers.callback_query(F.data == 'sell_token')
async def cmd_profile(callback: CallbackQuery):
    pass

# ---------------- HOME -------------------
@user_handlers.callback_query(F.data == 'home')
async def cmd_profile(callback: CallbackQuery, state:FSMContext):
    await state.clear()

    user_id = callback.from_user.id
    welcome_message = (
        '🎉 Welcome to the Fan Token Purchase Bot! 🎉\n\n'
        '🚀 This bot allows you to purchase fan tokens on the Solana network.\n'
        '🔐 A new Solana wallet will be created for you to manage your tokens.\n\n'
        '📌 Your public key will be displayed once your wallet is created.\n'
        '💡 If you have any questions or need assistance, feel free to ask!\n'
        '\n'
        'Get started by exploring the options below:'
    )

    if not db.user_exists(user_id):
        public_key, private_key = sol.create_wallet()
        db.add_user(user_id, private_key, public_key)
        welcome_message += f'\n\n🆕 Your new Solana wallet has been created!\n🔑 Public Key: `{public_key}`'

    await callback.message.edit_text(welcome_message, parse_mode='Markdown', reply_markup=kb.main)
