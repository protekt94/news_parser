import requests
from bs4 import BeautifulSoup
import json
import datetime
from news import news_xakep, news_antimalware


def check_news_update():
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
            article_desc = article.find("p").text.strip()
            article_date = ' '.join(url_id[:3])
            article_date = str(datetime.datetime.strptime(article_date, '%Y %m %d').date())
            news_dict[article_id] = {
                "article_title": article_title,
                "article_desc": article_desc,
                "article_url": article_url,
                "article_date": article_date
            }
            fresh_news[article_id] = {
                    "article_title": article_title,
                    "article_desc": article_desc,
                    "article_url": article_url,
                    "article_date": article_date
                }

    with open("news_dict.json", "w") as file:
        json.dump(news_dict, file, ensure_ascii=False, indent=4)

    return fresh_news


def main():
    check_news_update()


if __name__ == '__main__':
    main()
