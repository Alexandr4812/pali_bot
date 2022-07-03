import logging
import os

# Telegram bot token
token = os.environ.get('PALI_BOT_TOKEN', default='5151139838:AAF014XgtqS0_OgmzJNP5yEJ-gSWUUFw9mg')

# Maps commands to files in data/ dir
COMMAND_MAPPING = {
    'all_sutta': 'all_suttas.txt',
    'theragatha_sutta': 'theragatha.txt',
    'therigatha_sutta': 'theragatha.txt',
    'dhammapada_sutta': 'dhammapada.txt',
    'itivuttaka_sutta': 'itivuttaka.txt',
    'udana_sutta': 'udana.txt',
}

# Info text
about_text = (
    'Этот бот создан для некоммерческого использования, все материалы взяты с сайта theravada.ru.'
    '\n\n'
    'Наша <a href="https://theravada.ru/blessings.htm">община</a> существует на пожертвования,'
    ' вы можете сделать дану на карту сбербанка 4276 5500 2002 5576.'
    '\n\n'
    'По вопросам и предложениям пишите @Alexandr_Cherkaev и @Max_Kotebus')

log_level = logging.WARNING
