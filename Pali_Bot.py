import telebot
from config import mainconfig

########################################################

token = '5151139838:AAF014XgtqS0_OgmzJNP5yEJ-gSWUUFw9mg'
bot = telebot.TeleBot(token)

main_menu = """
Выберите раздел

Любой: /all_sutta
Дхаммапада: /dhammapada_sutta
Тхерагатха: /theragatha_sutta
Тхеригатха: /therigatha_sutta
Итивуттака: /itivuttaka_sutta
Удана: /udana_sutta

Инфо: /about_us"""

def get_text(sitemap, command):
    try:
        print_text = mainconfig(sitemap)
    except Exception as e:
        print_text = str(e) + "\nОШИБКА ПРОГРАММЫ\nНАЖМИТЕ: /start"

    return print_text + '\n\nСледующая сутта:  /' + command

@bot.message_handler(commands=['start'])
def main_menu_func(message):
    bot.send_message(message.chat.id, main_menu) \

@bot.message_handler(commands=['all_sutta'])
def all_sutta_func(message):
    print_text = get_text("all_suttas.txt", 'all_sutta')
    limit = 4000
    if len(print_text) >= limit:
        while print_text[limit] != '.':
            limit += 1
        else:
            limit += 1
            bot.send_message(message.chat.id, print_text[:limit], parse_mode="HTML")
            bot.send_message(message.chat.id, print_text[limit:], parse_mode="HTML")
    else:
        bot.send_message(message.chat.id, print_text, parse_mode="HTML")

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
    limit = 4000
    if len(print_text) >= limit:
        while print_text[limit] != '.':
            limit += 1
        else:
            limit +=1
            bot.send_message(message.chat.id, print_text[:limit], parse_mode="HTML")
            bot.send_message(message.chat.id, print_text[limit:], parse_mode="HTML")
    else:
        bot.send_message(message.chat.id, print_text, parse_mode="HTML")


@bot.message_handler(commands=['about_us'])
def about_us_func(message):
    print_text = 'Этот бот создан для некоммерческого использования, все материалы берутся с сайта theravada.ru.\n' \
                 'Наша <a href="https://theravada.ru/blessings.htm">община</a> существует на пожертвования, вы можете сделать дану на карту сбербанка 4276 5500 2002 5576.\n\n' \
                 'По вопросам и предложениям пишите @Alexandr_Cherkaev и @Max_Kotebus'
    bot.send_message(message.chat.id, print_text, parse_mode="HTML")


bot.polling(none_stop=True)
