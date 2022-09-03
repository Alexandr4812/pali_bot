import os

from telegram import ParseMode
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import Updater

import config


class Bot:
    def __init__(self, config_ = None):  # TODO Pass config
        DIR = os.path.abspath(os.path.dirname(__file__))

        self._config = config
        self._updater = Updater(token=config.TOKEN)
        dispatcher = self._updater.dispatcher

        dispatcher.add_handler(
            CommandHandler(
                command=['start', 'help'],
                callback=self._start_handler))
        dispatcher.add_handler(
            CommandHandler(
                command=list(config.COMMAND_MAPPING.keys()),
                callback=self._generic_get_random_handler))
        dispatcher.add_handler(
            CommandHandler(
                command='about',
                callback=self._about_handler))

    def run(self) -> None:
        self._updater.start_polling()
        self._updater.idle()

    def _start_handler(self, update: Update, context: CallbackContext) -> None:
        # TODO reply_markup=markup
        update.message.reply_text(config.GREETING_TEXT, parse_mode=ParseMode.HTML)


    def _generic_get_random_handler(self, update: Update, context: CallbackContext) -> None:
        command = telebot.util.extract_command(message.text)
        print_text = get_text(command)
        limit = 4050
        # TODO Use telegram module tool
        if len(print_text) >= limit:
            index = delimiter(print_text, limit)
            for x in range(0, len(index) - 1):
                bot.send_message(message.chat.id, print_text[index[x]:index[x + 1]])
            bot.send_message(message.chat.id, print_text[index[-1]:])
        else:
            bot.send_message(message.chat.id, print_text)


    def _about_handler(self, update: Update, context: CallbackContext) -> None:
        update.message.reply_text(self._config.ABOUT_TEXT, parse_mode=ParseMode.HTML)
