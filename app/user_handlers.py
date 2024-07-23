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
    welcome_message = 'Welcome to our bot'

    if not db.user_exists(user_id):
        db.add_user(user_id)
    await message.answer(welcome_message, parse_mode='Markdown', reply_markup=kb.main)

