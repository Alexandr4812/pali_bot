import os
import random

from typing import Dict

import telebot
import config

CACHE: Dict[str, str] = {}
telebot.logger.setLevel(config.log_level)

bot = telebot.TeleBot(config.token)


def mainconfig(txt_file):
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


def get_text(sitemap, command):
    try:
        text = mainconfig(sitemap)
    except FileNotFoundError as error:
        telebot.logger.exception(error, exc_info=error)
        text = 'Ошибка программы: файл не найден.\nНажмите /start для продолжения'

    return text + f'\n\nСледующая сутта: /{command}'


@bot.message_handler(commands=['start', 'help'])
def main_menu_func(message):
    # TODO reply_markup=markup
    bot.send_message(message.chat.id, config.main_menu)


@bot.message_handler(commands=['all_sutta'])
def all_sutta_func(message):
    print_text = get_text("all_suttas.txt", 'all_sutta')
    limit = 4050
    if len(print_text) >= limit:
        index = delimiter(print_text, limit)
        for x in range(0, len(index) - 1):
            bot.send_message(message.chat.id, print_text[index[x]:index[x + 1]], parse_mode="HTML")
        bot.send_message(message.chat.id, print_text[index[-1]:], parse_mode="HTML")
    else:
        bot.send_message(message.chat.id, print_text, parse_mode='HTML')


@bot.message_handler(commands=['theragatha_sutta'])
def theragatha_sutta_func(message):
    print_text = get_text("theragatha.txt", 'theragatha_sutta')
    bot.send_message(message.chat.id, print_text, parse_mode="HTML")


@bot.message_handler(commands=['therigatha_sutta'])
def therigatha_sutta_func(message):
    print_text = get_text("therigatha.txt", 'therigatha_sutta')
    bot.send_message(message.chat.id, print_text, parse_mode="HTML")


@bot.message_handler(commands=['dhammapada_sutta'])
def dhammapada_sutta_func(message):
    print_text = get_text("dhammapada.txt", 'dhammapada_sutta')
    bot.send_message(message.chat.id, print_text, parse_mode="HTML")


@bot.message_handler(commands=['itivuttaka_sutta'])
def itivuttaka_sutta_func(message):
    print_text = get_text("itivuttaka.txt", 'itivuttaka_sutta')
    bot.send_message(message.chat.id, print_text, parse_mode="HTML")


@bot.message_handler(commands=['udana_sutta'])
def udana_sutta_func(message):
    print_text = get_text("udana.txt", 'udana_sutta')
    limit = 4050
    if len(print_text) >= limit:
        com_index = print_text.index("<u>")
        index = delimiter(print_text, limit)
        for x in range(len(index) - 1):
            bot.send_message(message.chat.id, print_text[index[x]:index[x + 1]], parse_mode="HTML")
        bot.send_message(message.chat.id, print_text[index[-1]:com_index], parse_mode="HTML")
        bot.send_message(message.chat.id, print_text[com_index:], parse_mode="HTML")
    else:
        bot.send_message(message.chat.id, print_text, parse_mode='HTML')


@bot.message_handler(commands=['about_us'])
def about_us_func(message):
    bot.send_message(message.chat.id, config.about_text, parse_mode="HTML")


if __name__ == '__main__':
    bot.polling(none_stop=True)
