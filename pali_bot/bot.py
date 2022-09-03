import os

from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import Updater

import config

from pali_bot.sutta_provider import SuttaProvider
from pali_bot.utils import html_format_sutta
from pali_bot.utils import split_long_message


class RandomSuttaHandler:
    def __init__(self, section: str, sutta_provider: SuttaProvider):
        self._sutta_provider = sutta_provider
        self._section = section

    def __call__(self, update: Update, context: CallbackContext) -> None:
        sutta = self._sutta_provider.get_random_sutta(self._section)

        html_text = html_format_sutta(sutta)

        html_text += f'\n\u21E5 /{self._section}_sutta'

        for msg in split_long_message(html_text):
            update.message.reply_html(msg, disable_web_page_preview=True)


class Bot:
    def __init__(self, sutta_provider: SuttaProvider, config_=None):  # TODO Pass config
        self._config = config
        self._sutta_provider = sutta_provider
        self._updater = Updater(token=config.TOKEN)
        dispatcher = self._updater.dispatcher

        dispatcher.add_handler(
            CommandHandler(
                command=['start', 'help'],
                callback=self._start_handler))
        # TODO __all__
        for section in sutta_provider.sections:
            dispatcher.add_handler(
                CommandHandler(
                    command=f'{section}_sutta',
                    callback=RandomSuttaHandler(section, sutta_provider)))
        dispatcher.add_handler(
            CommandHandler(
                command='about',
                callback=self._about_handler))

    def run(self) -> None:
        self._updater.start_polling()
        self._updater.idle()

    def _start_handler(self, update: Update, _: CallbackContext) -> None:
        # TODO Build message
        update.message.reply_html(config.GREETING_TEXT)

    def _about_handler(self, update: Update, _: CallbackContext) -> None:
        update.message.reply_html(self._config.ABOUT_TEXT)
