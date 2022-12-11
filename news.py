import requests
from bs4 import BeautifulSoup
import json
import datetime


class GetNews:
    def __init__(self, headers, url):
        self.headers = headers
        self.url = url


news_xakep: GetNews = GetNews(
    headers={
        "user - agent": "Mozilla/5.0 (Windows NT 10.0; Win64;x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome "
                        "/106.0.0.0 Safari/537.36 "
    },
    url="https://xakep.ru/category/news/")

news_antimalware: GetNews = GetNews(
    headers={
        "user - agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/102.0.5005.167 YaBrowser/22.7.3.829 Yowser/2.5 Safari/537.36"},
    url='https://www.anti-malware.ru/news/'
)


def get_xakep_news():
    r = requests.get(url=news_xakep.url, headers=news_xakep.headers)

    soup = BeautifulSoup(r.text, "lxml")
    articles_cards = soup.find_all("div", class_="block-article bd-col-md-6 bdaiaFadeIn")

    xakep_news = {}
    for article in articles_cards:
        article_title = article.find("h3", class_="entry-title").text.strip()
        article_desc = article.find("p").text.strip()
        article_url = article.find("a").get("href")
        url_id = article_url.split("/")[-5:-1]
        article_date = ' '.join(url_id[:3])
        article_date = str(datetime.datetime.strptime(article_date, '%Y %m %d').date())
        article_id = url_id[3]

        xakep_news[article_id] = {
            "article_title": article_title,
            "article_desc": article_desc,
            "article_url": article_url,
            "article_date": article_date
        }
    with open("news_dict.json", "w") as file:
        json.dump(xakep_news, file, ensure_ascii=False, indent=4)


def get_antimalware_news():
    r = requests.get(url=news_antimalware.url, headers=news_antimalware.headers)

    soup = BeautifulSoup(r.text, "lxml")
    articles_cards = soup.find_all("div", class_="view-content")
    antimalware_news = {}
    for article in articles_cards:
        for i_article in article.find_all("div", class_='node node-news node-teaser clearfix'):
            article_title = i_article.find("h2").text
            article_desc = i_article.find("p").text.strip()
            article_url = i_article.find("a").get("href")
            article_date = article_url.split('/')[2].split('-')[:3]
            article_date = ' '.join(article_date)
            article_date = str(datetime.datetime.strptime(article_date, '%Y %m %d').date())

            article_id = article_url.split('/')[3]
            article_url = 'https://www.anti-malware.ru/' + article_url

            antimalware_news[article_id] = {
                "article_title": article_title,
                "article_desc": article_desc,
                "article_url": article_url,
                "article_date": article_date
            }
            with open('news_dict.json') as file:
                data = json.load(file)
                data.update(antimalware_news)
    with open('news_dict.json', 'w') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
