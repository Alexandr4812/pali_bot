import logging

import config

from pali_bot.bot import Bot


def main() -> None:
    logging.basicConfig(level=config.LOG_LEVEL)
    Bot().run()


if __name__ == '__main__':
    main()
