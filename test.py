from news import news_habr
import requests
from bs4 import BeautifulSoup
import json
import datetime


# @dp.message_handler(Text(equals='Все новости'))
# async def get_all_news(message: types.Message):
#     with open("news_dict.json") as file:
#         news_dict = json.load(file)
#     for k, v in sorted(news_dict.items()):
#         news = f"{hbold(v['article_date'])}\n" \
#                f"{hlink(v['article_title'], v['article_url'])}"
#         await message.answer(news)
#     with open("antimalware_news.json") as file:
#         antimalware_news = json.load(file)
#     for k, v in sorted(antimalware_news.items()):
#         news = f"{hbold(v['article_date'])}\n" \
#                f"{hlink(v['article_title'], v['article_url'])}"
#         await message.answer(news)
#
#
# @dp.message_handler(Text(equals='Последние 5 новостей'))
# async def get_five_last_news(message: types.Message):
#     with open("news_dict.json") as file:
#         news_dict = json.load(file)
#
#     for k, v in sorted(news_dict.items())[-5:]:
#         news = f"{hbold(k[:10])}\n" \
#                f"{hlink(v['article_title'], v['article_url'])}"
#         await message.answer(news)
#
#
# @dp.message_handler(Text(equals='Свежие новости'))
# async def get_fresh_news(message: types.Message):
#     fresh_news = check_news_update()
#     if len(fresh_news) >= 1:
#         for k, v in sorted(fresh_news.items()):
#             news = f"{hbold(k[:10])}\n" \
#                    f"{hlink(v['article_title'], v['article_url'])}"
#             await message.answer(news)
#     else:
#         await message.answer("Пока нет свежих новостей")
