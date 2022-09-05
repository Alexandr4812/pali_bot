import logging
import os

import config

from pali_bot.bot import Bot
from pali_bot.sutta_provider import SuttaProvider


def main() -> None:
    logging.basicConfig(level=config.LOG_LEVEL)
    DIR = os.path.abspath(os.path.dirname(__file__))  # TODO
    sutta_provider = SuttaProvider()  # TODO config
    bot = Bot(sutta_provider=sutta_provider)
    bot.run()


if __name__ == '__main__':
    main()
