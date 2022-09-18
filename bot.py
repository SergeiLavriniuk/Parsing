import json
from main import parser_data
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold, hlink

bot = Bot(token="5764593621:AAFDRtj-C5gpO7GED_9kyEyJi6EMijNW7rI", parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

@dp.message_handler(commands='start')
async def start(message: types.Message):
    start_button = ['Начать поиск']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_button)

    await message.answer("Обувь для мужчин", reply_markup=keyboard)

@dp.message_handler(Text(equals='Начать поиск'))
async def get_shoes(message: types.Message):
    await message.answer('Пожалуйста подождите, собираю информацию...')

    parser_data()

    with open('results.json', 'r') as file:
        reader = json.load(file)
    for item in reader:
        card = f"{hlink(item.get('code'), item.get('link'))}\n"\
            f"{hlink(item.get('card_image'), item.get('src'))}\n"\
            f"{hbold('Размеры: ')}{item.get('sizes')}\n" \
            f"{hbold('Цена: ')}{item.get('price')}\n"
        await message.answer(card)
        print(card)


def main():
    executor.start_polling(dp)

if __name__== '__main__':
    main()