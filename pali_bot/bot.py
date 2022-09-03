import os

from telegram import ParseMode
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import Updater
from telegram.constants import MAX_MESSAGE_LENGTH

import config

from pali_bot.sutta_provider import SuttaProvider


class RandomSuttaHandler:
    def __init__(self, section: str, sutta_provider: SuttaProvider):
        self._sutta_provider = sutta_provider
        self._section = section

    def __call__(self, update: Update, context: CallbackContext) -> None:
        sutta = self._sutta_provider.get_random_sutta(self._section)
        # TODO
        if len(print_text) >= limit:
            index = delimiter(print_text, limit)
            for x in range(0, len(index) - 1):
                bot.send_message(message.chat.id, print_text[index[x]:index[x + 1]])
            update.message.reply_html(print_text[index[-1]:])
        else:
            update.message.reply_html(sutta['text'])


class Bot:
    def __init__(self, sutta_provider: SuttaProvider, config_=None):  # TODO Pass config
        DIR = os.path.abspath(os.path.dirname(__file__))

        self._config = config
        self._sutta_provider = sutta_provider
        self._updater = Updater(token=config.TOKEN)
        dispatcher = self._updater.dispatcher

        dispatcher.add_handler(
            CommandHandler(
                command=['start', 'help'],
                callback=self._start_handler))
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

    def _start_handler(self, update: Update, context: CallbackContext) -> None:
        update.message.reply_html(config.GREETING_TEXT)

    def _about_handler(self, update: Update, context: CallbackContext) -> None:
        update.message.reply_html(self._config.ABOUT_TEXT)
