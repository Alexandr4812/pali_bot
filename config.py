import logging
import os

from utils import SectionEntry
from utils import get_greeting_text

# TODO Update


# Telegram bot token
TOKEN = os.environ.get(
    'PALI_BOT_TOKEN',
    default='5151139838:AAF014XgtqS0_OgmzJNP5yEJ-gSWUUFw9mg')  # FIXME Tokens in repo is a bad practice

LOG_LEVEL = logging.WARNING

# Maps commands to files in data/ dir
COMMAND_MAPPING = {
    'all_sutta': SectionEntry(
        filename='all_suttas.txt', displayname='Любой раздел'),
    'theragatha_sutta': SectionEntry(
        filename='theragatha.txt', displayname='Техрагатха'),
    'therigatha_sutta': SectionEntry(
        filename='therigatha.txt', displayname='Тхеригатха'),
    'dhammapada_sutta': SectionEntry(
        filename='dhammapada.txt', displayname='Дхаммапада'),
    'itivuttaka_sutta': SectionEntry(
        filename='itivuttaka.txt', displayname='Итивуттака'),
    'udana_sutta': SectionEntry(
        filename='udana.txt', displayname='Удана'),
}

# Info text
ABOUT_TEXT = (
    'Этот бот создан для некоммерческого использования, все материалы взяты с сайта theravada.ru.'
    '\n\n'
    'Наша <a href="https://theravada.ru/blessings.htm">община</a> существует на пожертвования,'
    ' вы можете сделать дану на карту сбербанка 4276 5500 2002 5576.'
    '\n\n'
    'По вопросам и предложениям пишите @Alexandr_Cherkaev, @Max_Kotebus, @bergentroll')

_GREETING_TEXT_TEMPLATE = '''
<b>Случайная сутта</b>

Получить случайную сутту из раздела:

{command_text}

Инфо: /about_us
Это сообщение: /help
'''

GREETING_TEXT = get_greeting_text(_GREETING_TEXT_TEMPLATE, COMMAND_MAPPING)
