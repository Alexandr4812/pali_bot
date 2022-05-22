import logging
import os
import random

from typing import Dict

import telebot

CACHE: Dict[str, str] = {}


def mainconfig(txt_file):
    with open(txt_file, 'r', encoding='cp1251') as f:
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
    сom_index = print_text.index('<u>')
    for x in range(0, сom_index, limit):
        i = print_text.index(" ", x, limit + x)
        index.append(i)
    return index


###################################################################
token = os.environ.get('PALI_BOT_TOKEN', default='5151139838:AAF014XgtqS0_OgmzJNP5yEJ-gSWUUFw9mg')

main_menu = """
Выберите раздел

Любой: /all_sutta
Дхаммапада: /dhammapada_sutta
Тхерагатха: /theragatha_sutta
Тхеригатха: /therigatha_sutta
Итивуттака: /itivuttaka_sutta
Удана: /udana_sutta

Инфо: /about_us"""

about_text = (
    'Этот бот создан для некоммерческого использования, все материалы взяты с сайта theravada.ru.'
    '\n\n'
    'Наша <a href="https://theravada.ru/blessings.htm">община</a> существует на пожертвования,'
    ' вы можете сделать дану на карту сбербанка 4276 5500 2002 5576.'
    '\n\n'
    'По вопросам и предложениям пишите @Alexandr_Cherkaev и @Max_Kotebus')

log_level = logging.WARNING

######################################################################

telebot.logger.setLevel(log_level)
