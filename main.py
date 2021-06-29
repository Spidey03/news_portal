import argparse
import sys

import gnureadline as gnureadline

from config.color_codes import Colors
from news import NewsSearch

page_no = 1


def list_commands():
    from config.commands_description import commands_description
    for func, desc in commands_description.items():
        print("{}{}{:<10}{}{}".format(Colors.BOLD, Colors.CYAN, func, Colors.ENDC, Colors.ENDC), end=" : ")
        print("{}{:}{}".format(Colors.WHITE, desc, Colors.ENDC))


def signal_handler(sig, frame):
    print("\nGoodbye!\n")
    sys.exit(0)


def _quit():
    print("GoodBye!!!")
    sys.exit(0)


def completer(text, state):
    options = [i for i in commands if i.startswith(text)]
    if state < len(options):
        return options[state]
    return None


def next_page():
    global page_no
    page_no += 1
    print(page_no)
    if not _prev_cmd:
        print("{}Invalid Command{}".format(Colors.RED, Colors.ENDC))
        return
    _prev_cmd(page_no=page_no)


def reset_page_no():
    global page_no
    page_no = 1


gnureadline.parse_and_bind('tab: complete')
gnureadline.set_completer(completer)

parser = argparse.ArgumentParser(description="")
parser.add_argument('-c', '--command', help='run in single command mode & execute provided command', action='store')

args = parser.parse_args()

news = NewsSearch()

commands = {
    "list": list_commands,
    "sources": news.get_sources,
    "headlines": news.get_top_headlines,
    "everything": news.get_all_news,
    "next": next_page,
    "exit": quit,
    "quit": quit
}

previous_commands = ["get_sources", "get_top_headlines", "get_all_news"]

_prev_cmd, _cmd = None, None

while True:
    if _cmd and _cmd.__name__ in previous_commands:
        _prev_cmd = _cmd
    elif _prev_cmd and _prev_cmd.__name__ == next_page:
        _prev_cmd = _prev_cmd
    else:
        reset_page_no()

    gnureadline.parse_and_bind("tab: complete")
    gnureadline.set_completer(completer)
    if args.command:
        cmd = args.command
        _cmd = commands.get(cmd)
    else:
        print("{}{}{}{}{}".format(Colors.BOLD, Colors.WARNING, "Run Command", Colors.ENDC, Colors.ENDC))
        cmd = input()
        _cmd = commands.get(cmd)

    if _cmd:
        sources = _cmd()
        if _cmd.__name__ == "get_sources":
            print("Enter Source Number: ", end="")
            source_id = input()
            print(sources.get(source_id))
            news.get_top_headlines(sources=sources.get(source_id)["name"])
    elif cmd == "":
        print("")
    else:
        print("{}{}{}".format(Colors.RED, "Unknown Command", Colors.ENDC))
