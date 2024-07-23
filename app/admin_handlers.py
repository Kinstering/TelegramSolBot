import asyncio
from aiogram import Bot, Dispatcher, F, types, Router
from aiogram.types import Message, CallbackQuery, ContentType
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton

from datetime import datetime
import random

import app.keyboard as kb
from app.db import Database
from config import TOKEN

admin_handlers = Router()
bot = Bot(token=TOKEN)
db = Database('database.db')

class AdminStates(StatesGroup):
    password = State()

    title_product_photo = State()
    title_product_name = State()
    title_product_price = State()

    product_photo = State()
    product_location = State()

def generate_unique_number():
    return int(''.join(random.choices('0123456789', k=9)))

@admin_handlers.message(F.text == '/admin')
async def cmd_admin(message: Message, state:FSMContext):
    await message.answer('Enter the access password to log in to the admin panel')

    await state.set_state(AdminStates.password)

@admin_handlers.message(AdminStates.password)
async def cmd_enter_password(message: Message, state:FSMContext):
    message_text = message.text

    if message_text == 'k1nsterBot1625':
        await message.answer('You have successfully logged in as an administrator', reply_markup=kb.admin)
        await state.clear()
    else:
        pass

@admin_handlers.callback_data(F.data == 'add_product')
async def cmd_add_product(callback:CallbackQuery):
    user_id = callback.from_user.id

    country_names = db.get_all_country_names()

    builder = InlineKeyboardBuilder()

    for country in country_names:
        country_name = country[0]
        button_text = country_name
        callback_data = f'add_product_country_{country_name}'
        builder.button(text=button_text, callback_data=callback_data)
    
    builder.adjust(1)
    markup = builder.as_markup(resize_keyboard=True)

    await callback.message.answer('🌍 Select a country for added product', reply_markup=markup)

@admin_handlers.callback_query(F.data.startswith('add_product_country_'))
async def cmd_country(callback:CallbackQuery):
    country = callback.data.split('_')[3]

    city_names = db.get_all_city_names(country)

    builder = InlineKeyboardBuilder()

    for city in city_names:
        city_name = city[0]
        button_text = city_name
        callback_data = f'add_product_city_{city_name}'
        builder.button(text=button_text, callback_data=callback_data)
    
    builder.adjust(1)
    markup = builder.as_markup(resize_keyboard=True)

    await callback.message.answer('🏙️ Select a city', reply_markup=markup)

@admin_handlers.callback_query(F.data.startswith('add_product_city_'))
async def cmd_country(callback:CallbackQuery):
    city = callback.data.split('_')[3]

    neighbourhood_names = db.get_all_neighbourhood_names(city)

    builder = InlineKeyboardBuilder()

    for neighbourhood in neighbourhood_names:
        neighbourhood_name = neighbourhood[0]
        button_text = neighbourhood_name
        callback_data = f'add_product_neighbourhood_{city}'
        builder.button(text=button_text, callback_data=callback_data)
    
    builder.adjust(1)
    markup = builder.as_markup(resize_keyboard=True)

    await callback.message.answer(f'🏙️ {city}\n◾️◾️◾️◾️◾️\nSelect a neighbourhood', reply_markup=markup)

@admin_handlers.callback_query(F.data.startswith('add_product_neighbourhood_'))
async def cmd_country(callback:CallbackQuery, state:FSMContext):
    neighbourhood = callback.data.split('_')[3]
    await state.update_data(neighbourhood=neighbourhood)

    await callback.message.answer(f'🏙️ {neighbourhood}\n◾️◾️◾️◾️◾️\n*Send please title product photo*\n(that photo that users will see when you click on a product)', parse_mode='Markdown', reply_markup=kb.admin_cancel)
    await state.set_state(AdminStates.title_product_photo)

@admin_handlers.message(AdminStates.title_product_photo)
async def cmd_title_photo(message:Message, state:FSMContext):
    try:
        photo = message.photo[-1]
        product_photo = photo.file_id
        await state.update_data(product_photo=product_photo)
        await message.answer('Great, now enter the *name* of the product.\n\nExample: `Sugar - 60g`', parse_mode='Markdown', reply_markup=kb.admin_cancel)
        await state.set_state(AdminStates.title_product_name)
    except Exception:
        await message.answer("The photo didn't process properly\n\nTry *compressing the image* when you send it.", parse_mode='Markdown', reply_markup=kb.admin_cancel)

        await state.set_state(AdminStates.title_product_name)

@admin_handlers.message(AdminStates.title_product_name)
async def cmd_title_name(message:Message, state:FSMContext):
    product_name = message.text
    await state.update_data(product_name = product_name)

    await message.answer('Good, the last step you need to take is to enter a *price* for your product.', parse_mode='Markdown', reply_markup=kb.admin_cancel)
    await state.set_state(AdminStates.title_product_price)

@admin_handlers.message(AdminStates.title_product_price)
async def cmd_title_name(message:Message, state:FSMContext):
    product_price = message.text

    data = await state.get_data()
    neighbourhood = data['neighbourhood']
    product_photo = data['product_photo']
    product_name = data['product_name']
    unique_number = generate_unique_number()

    db.add_title_product(product_photo, product_name, product_price, neighbourhood, unique_number)
    await message.answer('Congratulations!\n\nYou have successfully added a new product.', reply_markup=kb.admin)

    await state.clear()

# ADD EXITING PRODUCT

@admin_handlers.callback_query(F.data == 'add_existing_product')
async def cmd_add_existing_product(callback:CallbackQuery):
    user_id = callback.from_user.id

    country_names = db.get_all_country_names()

    builder = InlineKeyboardBuilder()

    for country in country_names:
        country_name = country[0]
        button_text = country_name
        callback_data = f'add_exiting_country_{country_name}'
        builder.button(text=button_text, callback_data=callback_data)
    
    builder.adjust(1)
    markup = builder.as_markup(resize_keyboard=True)

    await callback.message.answer('🌍 Select a country for added product', reply_markup=markup)

@admin_handlers.callback_query(F.data.startswith('add_exiting_country_'))
async def cmd_country(callback:CallbackQuery):
    country = callback.data.split('_')[3]

    city_names = db.get_all_city_names(country)

    builder = InlineKeyboardBuilder()

    for city in city_names:
        city_name = city[0]
        button_text = city_name
        callback_data = f'add_exiting_city_{city_name}'
        builder.button(text=button_text, callback_data=callback_data)
    
    builder.adjust(1)
    markup = builder.as_markup(resize_keyboard=True)

    await callback.message.answer('🏙️ Select a city', reply_markup=markup)

@admin_handlers.callback_query(F.data.startswith('add_exiting_city_'))
async def cmd_country(callback:CallbackQuery):
    city = callback.data.split('_')[3]

    neighbourhood_names = db.get_all_neighbourhood_names(city)

    builder = InlineKeyboardBuilder()

    for neighbourhood in neighbourhood_names:
        neighbourhood_name = neighbourhood[0]
        button_text = neighbourhood_name
        callback_data = f'add_exiting_neighbourhood_{city}'
        builder.button(text=button_text, callback_data=callback_data)
    
    builder.adjust(1)
    markup = builder.as_markup(resize_keyboard=True)

    await callback.message.answer(f'🏙️ {city}\n◾️◾️◾️◾️◾️\nSelect a neighbourhood', reply_markup=markup)

@admin_handlers.callback_query(F.data.startswith('add_exiting_neighbourhood_'))
async def cmd_country(callback:CallbackQuery, state:FSMContext):
    neighbourhood = callback.data.split('_')[3]
    await state.update_data(neighbourhood=neighbourhood)

    # Fetch all product details for the selected neighbourhood
    products = db.get_all_products(neighbourhood)

    builder = InlineKeyboardBuilder()

    for product in products:
        product_name = product[0]
        product_price = product[1]
        product_unique_number = product[2]
        
        button_text = f"{product_name} - ${product_price}"
        callback_data = f'product_exiting_{product_unique_number}'
        builder.button(text=button_text, callback_data=callback_data)

    builder.adjust(1)
    markup = builder.as_markup(resize_keyboard=True)

@admin_handlers.callback_query(F.data.startswith('product_exiting_'))
async def cmd_country(callback:CallbackQuery, state:FSMContext):
    unique_number = callback.data.split('_')[2]
    await state.update_data(unique_number=unique_number)

    data = await state.get_data()
    neighbourhood = data['neighbourhood']

    await callback.message.answer(f'🏙️ {neighbourhood}\n◾️◾️◾️◾️◾️\n*Send please product photo*\n(this is a photo of the location when the user will pay for their purchase.)', parse_mode='Markdown', reply_markup=kb.admin_cancel)
    await state.set_state(AdminStates.product_photo)

@admin_handlers.message(AdminStates.product_photo)
async def cmd_title_photo(message:Message, state:FSMContext):
    try:
        photo = message.photo[-1]
        product_photo = photo.file_id
        await state.update_data(product_photo=product_photo)
        await message.answer('Great. Now send the *location* for the product.', parse_mode='Markdown', reply_markup=kb.admin_cancel)
        await state.set_state(AdminStates.title_product_name)
    except Exception:
        await message.answer("The photo didn't process properly\n\nTry *compressing the image* when you send it.", parse_mode='Markdown', reply_markup=kb.admin_cancel)

        await state.set_state(AdminStates.title_product_name)

@admin_handlers.message(AdminStates.product_location)
async def cmd_title_photo(message:Message, state:FSMContext):
    location = message.text

    data = state.get_data()
    unique_number = data['unique_number']
    product_photo = data['product_photo']

    product = db.get_product_title(unique_number)

    if product:
        product_title_photo = product[0]
        product_title_name = product[1]
        product_title_price = product[2]
        product_neighbourhood = product[3]
        product_unique_number = product[4]

    db.add_product(product_photo, location, product_title_name, product_title_price, unique_number)

    await message.answer('You succecessfully added new product', reply_markup=kb.admin_cancel)

    # check this moment
    await state.set_state(AdminStates.product_photo)
