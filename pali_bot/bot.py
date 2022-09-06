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


class RandomSuttaHandler:
    def __init__(self, section: str, sutta_provider: SuttaProvider):
        self._sutta_provider = sutta_provider
        self._section = section

    def __call__(self, update: Update, context: CallbackContext) -> None:
        sutta = self._sutta_provider.get_random_sutta(self._section)

        html_text = ''
        html_text += html_format_sutta(sutta)

        html_text += f'\n\u21E5 /{self._section}_sutta'
        html_text += f'\n\n#{self._section} #sutta_bot'

        for msg in split_long_message(html_text):
            update.message.reply_html(msg, disable_web_page_preview=True)


class Bot:
    def __init__(self, sutta_provider: SuttaProvider, token: str, about_text: str):
        self._sutta_provider = sutta_provider
        self._about_text_html = about_text
        self._updater = Updater(token=token)
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

        self._help_message_html = self._make_html_help()

    def _make_html_help(self) -> str:
        command_list = [f'/{section}_sutta' for section in self._sutta_provider.sections]
        command_text = '\n'.join(command_list)

        return (
            '<b>Сутты палийского канона</b>\n'
            '\n'
            'Получить случайную сутту из раздела:\n'
            '\n'
            f'{command_text}\n'
            '\n'
            'О боте: /about\n'
            'Это сообщение: /help')

    def run(self) -> None:
        self._updater.start_polling()
        self._updater.idle()

    def _start_handler(self, update: Update, _: CallbackContext) -> None:
        update.message.reply_html(self._help_message_html, disable_web_page_preview=True)

    def _about_handler(self, update: Update, _: CallbackContext) -> None:
        update.message.reply_html(self._about_text_html, disable_web_page_preview=True)
