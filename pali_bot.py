import os
import random

from typing import Dict

import telebot
import config

CACHE: Dict[str, str] = {}
telebot.logger.setLevel(config.log_level)

bot = telebot.TeleBot(config.token, parse_mode='HTML')


def mainconfig(txt_file):
    # TODO Implement relative
    file_path = os.path.join('data', txt_file)
    with open(file_path, 'r', encoding='cp1251') as f:
        contents = CACHE.get(txt_file)
        if contents is None:
            contents = f.read()
            CACHE[txt_file] = contents

    text_split = contents.split('___separator___')
    sn = random.randint(0, len(text_split) - 1)
    result = text_split[sn]
    return result


def delimiter(print_text, limit):
    index = []
    com_index = print_text.index('<u>')
    for x in range(0, com_index, limit):
        i = print_text.index(" ", x, limit + x)
        index.append(i)
    return index


def get_text(command):
    try:
        sitemap = config.COMMAND_MAPPING[command].filename
        text = mainconfig(sitemap) + f'\n\nСледующая сутта: /{command}'
    except (FileNotFoundError, KeyError) as error:
        telebot.logger.exception(error, exc_info=error)
        text = (
            f'<b>Ошибка программы</b>: файл данных для /{command} не найден.'
            '\n'
            '\nНажмите /start для продолжения')

    return text


@bot.message_handler(commands=['start', 'help'])
def main_menu_func(message):
    # TODO reply_markup=markup

    commands_list = [f'{val.displayname}: /{key}' for key, val in config.COMMAND_MAPPING.items()]
    commands_text = '\n'.join(commands_list)
    greeting_text = f'''
<b>Случайная сутта</b>:

Получить случайную сутту из раздела:

{commands_text}

Инфо: /about_us
'''

    bot.send_message(message.chat.id, greeting_text)


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
def about_us_func(message):
    bot.send_message(message.chat.id, config.about_text)


if __name__ == '__main__':
    bot.polling(none_stop=True)
