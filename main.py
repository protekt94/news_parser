import requests
import json
from bs4 import BeautifulSoup
from config import settings


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


def check_news_update():
    with open("news_dict.json") as file:
        news_dict = json.load(file)

    headers = {
        "user - agent": "Mozilla/5.0 (Windows NT 10.0; Win64;x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome /106.0.0.0 Safari/537.36"
    }
    url = "https://xakep.ru/category/news/"
    r = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(r.text, "lxml")
    articles_cards = soup.find_all("div", class_="block-article bd-col-md-6 bdaiaFadeIn")
    fresh_news = {}
    for article in articles_cards:
        article_url = article.find("a").get("href")
        url_id = article_url.split("/")[-5:-1]
        article_id = ":".join(url_id)

        if article_id in news_dict:
            continue
        else:
            article_title = article.find("h3", class_="entry-title").text.strip()
            article_desc = article.find("p").text.strip()

            news_dict[article_id] = {
                "article_title": article_title,
                "article_desc": article_desc,
                "article_url": article_url
            }
            fresh_news[article_id] = {
                "article_title": article_title,
                "article_desc": article_desc,
                "article_url": article_url
            }

    with open("news_dict.json", "w") as file:
        json.dump(news_dict, file, ensure_ascii=False, indent=4)

    return fresh_news


def main():
    pass# get_xakep_news()
    # print(check_news_update())
    # get_antimalware_news()


if __name__ == '__main__':
    main()
