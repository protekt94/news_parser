from news import get_xakep_news, get_antimalware_news
from update_news import check_news_update


def main():
    # get_xakep_news()
    # get_antimalware_news()
    print(check_news_update())


if __name__ == '__main__':
    main()
