import telebot
from config import mainconfig, token, about_text, main_menu
########################################################

bot = telebot.TeleBot(token)

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
    bot.send_message(message.chat.id, about_text, parse_mode="HTML")


bot.polling(none_stop=True)
