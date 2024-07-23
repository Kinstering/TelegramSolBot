import asyncio

from aiogram import Bot, Dispatcher
from config import TOKEN
from app.user_handlers import user_handlers

bot = Bot(token=TOKEN)
dp = Dispatcher()
        
async def main():
    dp.include_router(user_handlers)
    await dp.start_polling(bot)
    
if __name__ == '__main__':
    asyncio.run(main())
    