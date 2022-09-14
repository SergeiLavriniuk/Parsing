import json
from parser import parser_data
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold, hlink

bot = Bot(token="5764593621:AAFDRtj-C5gpO7GED_9kyEyJi6EMijNW7rI")
dp = Dispatcher(bot)

@dp.message_handler(commands='start')
async def start(message: types.Message):
    start_button = ['Начать поиск']
    await message.answer('Здравствуйте, хотите найти обувь Marko?')
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_button)
    await message.answer("Обувь для мужчин",reply_markup=keyboard)

@dp.message_handler(Text(equals='Начать поиск'))
async def get_shoes(message: types.Message):
    await message.answer('Please wait...')

    parser_data()

    with open('Results.csv') as file:
        data = json.load(file)

    for item in data:
        card = f"{hlink(item.get('CODE'), item.get('LINK'))}\n" \
            f"{hbold('Размеры: ')} {item.get('SIZES')}\n" \
            f"{hbold('Цена: ')} {item.get('PRICE')}\n" \
            f"{hlink(item.get('IMAGE'))}"

        await message.answer(card)


def main():
    executor.start_polling(dp)

if __name__== '__main__':
    main()