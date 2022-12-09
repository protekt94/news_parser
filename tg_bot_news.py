import asyncio
import json
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import hbold, hunderline, hcode, hlink
from aiogram.dispatcher.filters import Text

import config
from config import settings
from main import check_news_update
from loguru import logger

logger.add(
    config.settings["LOG_FILE"],
    format="{timee} {level} {message}",
    level="DEBUG",
    rotation="1 week",
    compression="zip"
)


class CyberNewsBot(Bot):
    def __int__(self, token, parse_mode):
        super().__int__(token, parse_mode=parse_mode)


bot: CyberNewsBot = CyberNewsBot(
    token=config.settings['TOKEN'],
    parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands="start")
async def start(message_from: types.Message) -> None:
    start_button = ["Все новости", "Последние 10 новостей", "Свежие новости"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_button)
    user_id: str = str(message_from.from_id)
    message = f"Лента новостей"
    try:
        await message_from.answer(message, reply_markup=keyboard)
    except Exception as send_error:
        logger.debug(f"{send_error.message}: Trouble id: {user_id}")
        return


@dp.message_handler(Text(equals='Все новости'))
async def get_all_news(message: types.Message):
    with open("news_dict.json") as file:
        news_dict = json.load(file)
    for k, v in sorted(news_dict.items()):
        news = f"{hbold(v['article_date'])}\n" \
               f"{hlink(v['article_title'], v['article_url'])}"
        await message.answer(news)
    with open("antimalware_news.json") as file:
        antimalware_news = json.load(file)
    for k, v in sorted(antimalware_news.items()):
        news = f"{hbold(v['article_date'])}\n" \
               f"{hlink(v['article_title'], v['article_url'])}"
        await message.answer(news)


@dp.message_handler(Text(equals='Последние 5 новостей'))
async def get_five_last_news(message: types.Message):
    with open("news_dict.json") as file:
        news_dict = json.load(file)

    for k, v in sorted(news_dict.items())[-5:]:
        news = f"{hbold(k[:10])}\n" \
               f"{hlink(v['article_title'], v['article_url'])}"
        await message.answer(news)


@dp.message_handler(Text(equals='Свежие новости'))
async def get_fresh_news(message: types.Message):
    fresh_news = check_news_update()
    if len(fresh_news) >= 1:
        for k, v in sorted(fresh_news.items()):
            news = f"{hbold(k[:10])}\n" \
                   f"{hlink(v['article_title'], v['article_url'])}"
            await message.answer(news)
    else:
        await message.answer("Пока нет свежих новостей")


async def news_every_minute():
    while True:
        fresh_news = check_news_update()
        if len(fresh_news) >= 1:
            for k, v in sorted(fresh_news.items()):
                news = f"{hbold(k[:10])}\n" \
                       f"{hlink(v['article_title'], v['article_url'])}"
                await bot.send_message(settings['user_id'], news, disable_notification=True)
        else:
            await bot.send_message(settings['user_id'], 'Пока свежих новостей нет')

        await asyncio.sleep(40)


if __name__ == '__main__':
    # loop = asyncio.get_event_loop()
    # loop.create_task(news_every_minute())
    executor.start_polling(dp, skip_updates=True)
