import requests
from bs4 import BeautifulSoup
import json
import datetime
from news import news_xakep, news_antimalware, news_habr


def check_news_update_xakep():
    with open("news_dict.json") as file:
        news_dict = json.load(file)
    r = requests.get(url=news_xakep.url, headers=news_xakep.headers)

    soup = BeautifulSoup(r.text, "lxml")
    articles_cards = soup.find_all("div", class_="block-article bd-col-md-6 bdaiaFadeIn")
    fresh_news = {}
    for article in articles_cards:
        article_url = article.find("a").get("href")
        url_id = article_url.split("/")[-5:-1]
        article_id = url_id[3]
        if article_id in news_dict:
            continue
        else:
            article_title = article.find("h3", class_="entry-title").text.strip()
            article_date = ' '.join(url_id[:3])
            article_date = str(datetime.datetime.strptime(article_date, '%Y %m %d').date())
            news_dict[article_id] = {
                "article_title": article_title,
                "article_url": article_url,
                "article_date": article_date
            }
            fresh_news[article_id] = {
                "article_title": article_title,
                "article_url": article_url,
                "article_date": article_date
            }

    with open("news_dict.json", "w") as file:
        json.dump(news_dict, file, ensure_ascii=False, indent=4)
    return fresh_news


def check_news_update_antimalware():
    with open("news_dict.json") as file:
        news_dict = json.load(file)

    r = requests.get(url=news_antimalware.url, headers=news_antimalware.headers)
    fresh_news = check_news_update_xakep()
    soup = BeautifulSoup(r.text, "lxml")
    articles_cards = soup.find_all("div", class_="view-content")
    with open('news_dict.json'):
        for article in articles_cards:
            for i_article in article.find_all("div", class_='node node-news node-teaser clearfix'):
                article_url = i_article.find("a").get("href")
                article_id = article_url.split('/')[3]
                if article_id in news_dict:
                    continue
                else:
                    article_title = i_article.find("h2").text
                    article_date = article_url.split('/')[2].split('-')[:3]
                    article_date = ' '.join(article_date)
                    article_date = str(datetime.datetime.strptime(article_date, '%Y %m %d').date())
                    article_url = 'https://www.anti-malware.ru/' + article_url

                    news_dict[article_id] = {
                        "article_title": article_title,
                        "article_url": article_url,
                        "article_date": article_date
                    }
                    fresh_news[article_id] = {
                        "article_title": article_title,
                        "article_url": article_url,
                        "article_date": article_date
                    }
                news_dict.update(fresh_news)
    with open('news_dict.json', 'w+') as file:
        json.dump(news_dict, file, ensure_ascii=False, indent=4)
    return fresh_news


def check_news_update_habr():
    with open("news_dict.json") as file:
        news_dict = json.load(file)

    r = requests.get(url=news_habr.url, headers=news_habr.headers)
    soup = BeautifulSoup(r.text, "lxml")
    articles_cards = soup.find_all("article", class_="tm-articles-list__item")
    fresh_news = check_news_update_antimalware()
    with open('news_dict.json'):
        for article in articles_cards:
            article_url = article.find("a", class_="tm-article-snippet__title-link").get("href")
            article_url = f"https://habr.com{article_url}"
            article_id = article.get("id")
            if article_id in news_dict:
                continue
            else:
                article_title = article.find("h2").text.strip()
                article_date = article.find("time").get("datetime")
                article_date = str(datetime.datetime.strptime(article_date, "%Y-%m-%dT%H:%M:%S.%fZ").date())

                news_dict[article_id] = {
                    "article_title": article_title,
                    "article_url": article_url,
                    "article_date": article_date
                }
                fresh_news[article_id] = {
                    "article_title": article_title,
                    "article_url": article_url,
                    "article_date": article_date
                }

            news_dict.update(fresh_news)

    with open('news_dict.json', 'w') as file:
        json.dump(news_dict, file, ensure_ascii=False, indent=4)

    return fresh_news
