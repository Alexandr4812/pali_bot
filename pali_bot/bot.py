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

from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import Updater

from pali_bot.sutta_provider import SuttaProvider
from pali_bot.utils import html_format_sutta
from pali_bot.utils import split_long_message


class GetSuttaHandler:
    """ Handle getting sutta commands
    """
    def __init__(self, section: str, sutta_provider: SuttaProvider):
        self._sutta_provider = sutta_provider
        self._section = section

    def __call__(self, update: Update, context: CallbackContext) -> None:
        num = None

        assert isinstance(context.args, list)
        assert update is not None

        if len(context.args) > 0:
            try:
                num = int(context.args[0], base=10)
            except (ValueError, TypeError):
                update.message.reply_html('<i>Command arg expected to be a number</i>')
                return
            sec_len = self._sutta_provider.get_section_length(self._section)
            if num > sec_len or num < 1:
                update.message.reply_html(
                    f'<i>{self._section} section contains only {sec_len} texts, '
                    f'arg should be in [1, {sec_len}]</i>')
                return
            sutta = self._sutta_provider.get_sutta(self._section, num)
        else:
            sutta = self._sutta_provider.get_random_sutta(self._section)

        html_text = ''
        html_text += html_format_sutta(sutta)

        html_text += f'\n\u21E5 /{self._section}_sutta'
        html_text += f'\n\n#{self._section} #sutta_bot'

        for msg in split_long_message(html_text):
            update.message.reply_html(msg, disable_web_page_preview=True)


class Bot:
    """ Handle commands from Telegram
    """
    def __init__(self, sutta_provider: SuttaProvider, token: str, about_text='', help_text=''):
        self._sutta_provider = sutta_provider
        self._updater = Updater(token=token)
        self._about_text_html = about_text
        self._help_text_html = help_text
        dispatcher = self._updater.dispatcher

        dispatcher.add_handler(
            CommandHandler(
                command=['start', 'help'],
                callback=self._start_handler))
        for section in sutta_provider.sections:
            dispatcher.add_handler(
                CommandHandler(
                    command=f'{section}_sutta',
                    callback=GetSuttaHandler(section, sutta_provider)))
        dispatcher.add_handler(
            CommandHandler(
                command='about',
                callback=self._about_handler))

    def run(self) -> None:
        """ Run polling
        """
        self._updater.start_polling()
        self._updater.idle()

    def _start_handler(self, update: Update, _: CallbackContext) -> None:
        update.message.reply_html(self._help_text_html, disable_web_page_preview=True)

    def _about_handler(self, update: Update, _: CallbackContext) -> None:
        update.message.reply_html(self._about_text_html, disable_web_page_preview=True)
