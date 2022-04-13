from aiofiles import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from main import get_data

bot = Bot(token="5101140976:AAH30JRB2cRKBSdTfjAkzt-pZr9XGZS3g38")
dp = Dispatcher(bot)

@dp.message_handler(commands='start')
async def start(message: types.Message):
    start_buttons = ['FOOTWEAR', 'PANTS', 'BAGS&PACKS', 'SHIRTS']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await message.answer('Choose category:', reply_markup=keyboard)
    

@dp.message_handler(Text(equals='BAGS&PACKS'))    
async def bag(message: types.Message):
    URL: str = "https://www.511tactical.com/eu-en/new/bags-packs.html?p=1"
    await message.answer('Please waiting...')
    chat_id = message.chat.id
    await send_data(URL, chat_id=chat_id)


@dp.message_handler(Text(equals='FOOTWEAR'))    
async def bag(message: types.Message):
    URL: str = "https://www.511tactical.com/eu-en/footwear/sa.html?p=1"
    await message.answer('Please waiting...')
    chat_id = message.chat.id
    await send_data(URL, chat_id=chat_id)


@dp.message_handler(Text(equals='PANTS'))    
async def bag(message: types.Message):
    URL: str = "https://www.511tactical.com/eu-en/mens/mens-pants.html?p=1"
    await message.answer('Please waiting...')
    chat_id = message.chat.id
    await send_data(URL, chat_id=chat_id)


@dp.message_handler(Text(equals='SHIRTS'))    
async def bag(message: types.Message):
    URL: str = "https://www.511tactical.com/eu-en/mens/mens-shirts.html?p=1"
    await message.answer('Please waiting...')
    chat_id = message.chat.id
    await send_data(URL, chat_id=chat_id)

    
async def send_data(url, chat_id):
    headers: dict = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36", "Accept": "*/*"}
    file = get_data(url, headers)
    print(file)
    await bot.send_document(chat_id=chat_id, document=open(file, 'rb'))
    await os.remove(file)

    
if __name__ == '__main__':
    executor.start_polling(dp)
