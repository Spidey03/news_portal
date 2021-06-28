import textwrap

from newsapi import NewsApiClient


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    BLACK = '\033[30m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'


class NewsSearch:
    def __init__(self):
        self.width = 100
        self.news_api = NewsApiClient(
            api_key=self.api_key
        )

    def get_top_headlines(
            self, q: str = None, qintitle: str = None, sources: str = None,
            language: str = "en", country: str = "in", category: str = None
    ):
        top_headlines = self.news_api.get_top_headlines(
            q=q, qintitle=qintitle, sources=sources,
            language=language, country=country, category=category,
            page=1, page_size=20
        )
        self.print_news(news=top_headlines)

    @property
    def api_key(self):
        from get_api_key import get_api_key
        return get_api_key()

    def print_news(self, news):
        print("Total Results Found: {}".format(news["totalResults"]))
        # print(json.dumps(news, indent=4))

        for news_item in news["articles"]:
            self._print_decoration()
            self._print_title(news_item)
            self._print_description(news_item)
            self._print_content(news_item)
            self._print_url(news_item)
            self._print_decoration()
            print()

    @staticmethod
    def _print_url(news_item):
        url = news_item.get("url")
        print("| {}{:<100}{:>} ".format(bcolors.BLACK, url, bcolors.ENDC))

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
        print("| {}{:<100}{:>} ".format(bcolors.YELLOW, news_content, bcolors.ENDC))

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
        print("| {}{:>100}{:>} ".format(bcolors.CYAN, news_description, bcolors.ENDC))

    def _print_title(self, news_item):
        title = textwrap.shorten(news_item.get("title", ""), self.width)
        print("| {}{:<100}{:>} ".format(bcolors.HEADER, title, bcolors.ENDC))

    def _print_decoration(self):
        print("{:<} {:} {:>}".format('+', '-' * self.width, '+'))


news = NewsSearch()
print(news.get_top_headlines())
