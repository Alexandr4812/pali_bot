#! /usr/bin/env python3

# Copyright 2022 Alexandr Cherkaev, Anton Karmanov <a.karmanov@inventati.org>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging

from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import Updater

from pali_bot.sutta_provider import SuttaProvider
from pali_bot.utils import html_format_sutta
from pali_bot.utils import split_long_message


class Bot:
    """ Handle commands from Telegram
    """
    def __init__(self, sutta_provider: SuttaProvider, token: str, about_text='', help_text=''):
        self._sutta_provider = sutta_provider
        self._updater = Updater(token=token)
        self._about_text_html = about_text
        self._help_text_html = help_text
        self._logger = logging.getLogger(f'{__name__}.{self.__class__.__name__}')
        self._access_logger = logging.getLogger(f'{__name__.split(".")[0]}.ACCESS')

        dispatcher = self._updater.dispatcher

        dispatcher.add_handler(
            MessageHandler(
                filters=(
                    ~Filters.update.edited_message &
                    Filters.regex('/.+')),
                callback=self._logger_handler),
            group=1)
        dispatcher.add_handler(
            CommandHandler(
                command=['start', 'help'],
                filters=(~Filters.update.edited_message),
                callback=self._start_handler))
        dispatcher.add_handler(
            MessageHandler(
                filters=(
                    ~Filters.update.edited_message &
                    Filters.regex('^/(.+)_sutta_(\\d+)$')),
                callback=self._sutta_handler))
        dispatcher.add_handler(
            MessageHandler(
                filters=(
                    ~Filters.update.edited_message &
                    Filters.regex('^/(.+)_sutta$')),
                callback=self._random_sutta_handler))
        dispatcher.add_handler(
            CommandHandler(
                command='about',
                filters=(~Filters.update.edited_message),
                callback=self._about_handler))

    def run(self) -> None:
        """ Run polling
        """
        self._updater.start_polling()
        self._updater.idle()

    def _logger_handler(self, update: Update, context: CallbackContext) -> None:
        assert isinstance(context.matches, list)
        match = context.matches[0]
        assert update.message is not None
        self._access_logger.info('Command %s in chat %s', match.string, update.message.chat_id)

    def _start_handler(self, update: Update, _: CallbackContext) -> None:
        update.message.reply_html(self._help_text_html, disable_web_page_preview=True)

    def _about_handler(self, update: Update, _: CallbackContext) -> None:
        update.message.reply_html(self._about_text_html, disable_web_page_preview=True)

    def _sutta_handler(self, update: Update, context: CallbackContext) -> None:
        assert isinstance(context.matches, list)
        match = context.matches[0]
        section = match.groups()[0]
        number = int(match.groups()[1])

        try:
            sec_len = self._sutta_provider.get_section_length(section)
        except KeyError:
            update.message.reply_html(f'<i>Unknown section "{section}", see /help</i>')
            return

        try:
            sutta = self._sutta_provider.get_sutta(section, number)
        except IndexError:
            update.message.reply_html(
                f'<i>{section} section contains only {sec_len} texts, '
                f'a number should be in [1, {sec_len}]</i>')
            return

        next_num = (number + 1) % sec_len
        html_text = html_format_sutta(sutta)
        html_text += f'\n\u21E5 /{section}_sutta_{next_num}'
        html_text += f'\n\n#{section} #sutta_bot'
        for msg in split_long_message(html_text):
            update.message.reply_html(msg, disable_web_page_preview=True)

    def _random_sutta_handler(self, update: Update, context: CallbackContext) -> None:
        assert isinstance(context.matches, list)
        match = context.matches[0]
        section = match.groups()[0]

        try:
            sutta = self._sutta_provider.get_random_sutta(section)
        except KeyError:
            update.message.reply_html(f'<i>Unknown section "{section}", see /help</i>')
            return

        html_text = html_format_sutta(sutta)

        html_text += f'\n\u21E5 /{section}_sutta'
        html_text += f'\n\n#{section} #sutta_bot'
        for msg in split_long_message(html_text):
            update.message.reply_html(msg, disable_web_page_preview=True)
