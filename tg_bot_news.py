import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import hbold, hlink
import config
from config import settings
from settings import settings
from update_news import check_news_update_habr, check_news_update_xakep, check_news_update_antimalware
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
    token=settings.settings['TOKEN'],
    parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands="start")
async def start(message_from: types.Message) -> None:
    user_id: str = str(message_from.from_id)
    message = (
        f"Лента новостей\n"
        f"Тут буду появляться новости с сайтов xakep.ru, anti-malware.ru\n"
        f"Обновление происходит каждые 15 минут\n"
               )
    try:
        await message_from.answer(message)
    except Exception:
        return


async def news_every_minute():
    while True:
        fresh_news = check_news_update_xakep()
        fresh_news.update(check_news_update_antimalware())
        fresh_news.update(check_news_update_habr())
        if len(fresh_news) >= 1:
            for k, v in sorted(fresh_news.items()):
                news = f"{hbold(v['article_date'])}\n" \
                       f"{hlink(v['article_title'], v['article_url'])}"
                try:
                    await bot.send_message(settings['channel_id'], news, disable_notification=True)
                except Exception:
                    return
        await asyncio.sleep(900)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(news_every_minute())
    executor.start_polling(dp, skip_updates=True)
