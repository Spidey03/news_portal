import datetime
import json
import textwrap
from typing import Union

from newsapi import NewsApiClient

from config.color_codes import Colors


class NewsSearch:
    def __init__(self):
        self.width = 150
        self.news_api = NewsApiClient(
            api_key=self.api_key
        )

    def get_top_headlines(
            self, q: str = None, qintitle: str = None, sources: str = None,
            language: str = "en", country: str = "in", category: str = None,
            page_no: int = 1
    ):
        top_headlines = self.news_api.get_top_headlines(
            q=q, qintitle=qintitle, sources=sources,
            language=language, country=country, category=category,
            page=page_no, page_size=20
        )
        self.print_news(news=top_headlines)

    def get_all_news(
            self, q: str = None, qintitle: str = None, sources: str = None,
            language: str = "en",
            from_date: Union[datetime.datetime, datetime.date, int, float] = None,
            to_date: Union[datetime.datetime, datetime.date, int, float] = None,
            page_no: int = 1, sort_by: str = None
    ):
        news = self.news_api.get_everything(
            q=q, qintitle=qintitle, sources=sources,
            language=language, from_param=from_date, to=to_date,
            sort_by=sort_by, page=page_no, page_size=30
        )
        self.print_news(news=news)

    def get_sources(
            self, category: str = None,
            language: str = "en", country: str = None
    ):
        sources = self.news_api.get_sources(
            category=category, language=language, country=country
        )
        self.print_sources(sources=sources["sources"])

    @property
    def api_key(self):
        from get_api_key import get_api_key
        return get_api_key()

    def print_news(self, news):
        print("Total Results Found: {}".format(news["totalResults"]))
        print(json.dumps(news, indent=4))
        for news_item in news["articles"]:
            self._print_decoration()
            self._print_title(news_item)
            self._print_description(news_item)
            self._print_content(news_item)
            self._print_url(news_item)
            self._print_datetime(news_item)
            self._print_decoration()
            self._print_new_line()

    def print_sources(self, sources):
        for source in sources:
            self._print_decoration()
            self._print_name(name=source.get("name"))
            self._print_decoration()

    @staticmethod
    def _print_url(news_item):
        url = news_item.get("url")
        w = textwrap.TextWrapper(
            width=150,
            max_lines=1,
            subsequent_indent="| ",
            fix_sentence_endings=True
        )
        news_url = w.fill(url)
        print("| {}{:<}{}".format(Colors.OKGREEN, "Click Below to Read More!!!", Colors.ENDC))
        print("| {}{:<150}{:>} ".format(Colors.BLUE, news_url, Colors.ENDC))

    def _print_content(self, news_item):
        w = textwrap.TextWrapper(
            width=self.width,
            max_lines=5,
            subsequent_indent="| ", fix_sentence_endings=True
        )
        content = ""
        if news_item["content"]:
            content = news_item["content"]
        news_content = w.fill(' '.join(content.strip().split()))
        print("| {}{:<150}{:>} ".format(Colors.YELLOW, news_content, Colors.ENDC))

    def _print_description(self, news_item):
        w = textwrap.TextWrapper(
            width=self.width,
            max_lines=2,
            subsequent_indent="| ",
            fix_sentence_endings=True
        )
        description = ""
        if news_item.get("description"):
            description = news_item["description"]
        news_description = w.fill(' '.join(description.strip().split()))
        print("| {}{:<150}{:>} ".format(Colors.CYAN, news_description, Colors.ENDC))

    def _print_title(self, news_item):
        title = textwrap.shorten(news_item.get("title", ""), self.width)
        print("| {}{:<150}{:>} ".format(Colors.HEADER, title, Colors.ENDC))

    def _print_decoration(self):
        print("{:<} {:} {:>}".format('+', '-' * self.width, '+'))

    @staticmethod
    def _print_new_line():
        print()

    @staticmethod
    def _print_datetime(news_item):
        if news_item.get("publishedAt"):
            published_at = news_item["publishedAt"]
            print("| {}{:>150}{:>} ".format(Colors.WHITE, published_at, Colors.ENDC))

    def _print_name(self, name):
        pass


if __name__ == "__main__":
    news = NewsSearch()
    news.get_sources()
