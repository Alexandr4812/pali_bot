import logging
import os

from typing import List

# Telegram bot token
token = os.environ.get('PALI_BOT_TOKEN', default='5151139838:AAF014XgtqS0_OgmzJNP5yEJ-gSWUUFw9mg')


class SectionEntry:
    def __init__(self, filename: str, displayname: str, tags: List[str] = None):
        if tags is None:
            tags = []

        self.filename = filename
        self.displayname = displayname


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
about_text = (
    'Этот бот создан для некоммерческого использования, все материалы взяты с сайта theravada.ru.'
    '\n\n'
    'Наша <a href="https://theravada.ru/blessings.htm">община</a> существует на пожертвования,'
    ' вы можете сделать дану на карту сбербанка 4276 5500 2002 5576.'
    '\n\n'
    'По вопросам и предложениям пишите @Alexandr_Cherkaev, @Max_Kotebus, @bergentroll')

log_level = logging.WARNING
