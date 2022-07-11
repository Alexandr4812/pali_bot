import os
import random

from typing import Dict
from typing import List

import telebot
import config

CACHE: Dict[str, str] = {}
telebot.logger.setLevel(config.LOG_LEVEL)

bot = telebot.TeleBot(config.TOKEN, parse_mode='HTML')

# Directory of the module
DIR = os.path.abspath(os.path.dirname(__file__))


def random_sutta(txt_file: str) -> str:
    file_path = os.path.join(DIR, 'data', txt_file)
    with open(file_path, 'r', encoding='cp1251') as f:
        contents = CACHE.get(txt_file)
        if contents is None:
            contents = f.read()
            CACHE[txt_file] = contents

    text_split = contents.split('___separator___')
    sn = random.randint(0, len(text_split) - 1)
    result = text_split[sn]
    return result


def delimiter(print_text: str, limit: int) -> List:
    index = []
    com_index = print_text.index('<u>')
    for x in range(0, com_index, limit):
        i = print_text.index(" ", x, limit + x)
        index.append(i)
    return index


def get_text(command: str) -> str:
    try:
        sitemap = config.COMMAND_MAPPING[command].filename
        text = random_sutta(sitemap) + f'\n\nСледующая сутта: /{command}'
    except (FileNotFoundError, KeyError) as error:
        telebot.logger.exception(error, exc_info=error)
        text = (
            f'<b>Ошибка программы</b>: файл данных для /{command} не найден.'
            '\n'
            '\nНажмите /start для продолжения')

    return text


@bot.message_handler(commands=['start', 'help'])
def main_menu_func(message) -> None:
    # TODO reply_markup=markup
    bot.send_message(message.chat.id, config.GREETING_TEXT)


@bot.message_handler(commands=list(config.COMMAND_MAPPING.keys()))
def generic_command(message: telebot.types.Message) -> None:
    command = telebot.util.extract_command(message.text)
    print_text = get_text(command)
    limit = 4050
    # TODO Use telebot tools
    # See https://pypi.org/project/pyTelegramBotAPI/#sending-large-text-messages
    if len(print_text) >= limit:
        index = delimiter(print_text, limit)
        for x in range(0, len(index) - 1):
            bot.send_message(message.chat.id, print_text[index[x]:index[x + 1]])
        bot.send_message(message.chat.id, print_text[index[-1]:])
    else:
        bot.send_message(message.chat.id, print_text)


@bot.message_handler(commands=['about_us'])
def about_us_func(message) -> None:
    bot.send_message(message.chat.id, config.ABOUT_TEXT)


if __name__ == '__main__':
    bot.polling(none_stop=True)
