import config
import telebot
from telebot import types # Button
from string import Template

bot = telebot.TeleBot(config.TOKEN)

user_dict = {}

class User:
    def __init__(self, city):
        self.city = city

        keys = ['fullname', 'phone', 'yuk_Hajmi', 'qayerdan', 'qayerga', 'yuk_Turi', 'Xizmat_haqi', 'boshlangich_tulov', 'qushimcha_malumot']
        
        for key in keys:
            self.key = None

# если /help, /start
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    itembtn2 = types.KeyboardButton('/elon_berish')
    itembtn1 = types.KeyboardButton('/Biz_haqimizda')
    markup.add(itembtn2, itembtn1)
    
    bot.send_message(message.chat.id, "Assalomu Alaykum "
    + message.from_user.first_name
    + " Ushbu Bot orqali siz o'z e'lonlaringizni berishingiz mumkin!", reply_markup=markup)

# /about
@bot.message_handler(commands=['Biz_haqimizda'])
def send_about(message):
	bot.send_message(message.chat.id, "Companiyamiz Logistica bozorida" 
    + " 1 yildan buyon faoliyat yuritib kelmoqda!")

# /reg
@bot.message_handler(commands=["elon_berish"])

def process_city_step(message):
    try:
        chat_id = message.chat.id
        user_dict[chat_id] = User(message.text)

                # удалить старую клавиатуру
        markup = types.ReplyKeyboardRemove(selective=False)

        msg = bot.send_message(chat_id, 'Familiya Ism Sharifingiz:', reply_markup=markup)
        bot.register_next_step_handler(msg, process_fullname_step)

    except Exception as e:
        bot.reply_to(message, 'ooops!!')

def process_fullname_step(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.fullname = message.text

        msg = bot.send_message(chat_id, 'Qayerdan:')
        bot.register_next_step_handler(msg, process_qayerdan_step)

    except Exception as e:
        bot.reply_to(message, 'ooops!!')


def process_qayerdan_step(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.qayerdan = message.text

        msg = bot.send_message(chat_id, 'Qayerga:')
        bot.register_next_step_handler(msg, process_qayerga_step)

    except Exception as e:
        bot.reply_to(message, 'ooops!!')

def process_qayerga_step(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.qayerga = message.text

        msg = bot.send_message(chat_id, 'Yukingizni turi:')
        bot.register_next_step_handler(msg, process_turi_step)

    except Exception as e:
        bot.reply_to(message, 'ooops!!')

def process_turi_step(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.yuk_Turi = message.text

        msg = bot.send_message(chat_id, 'Yukingiz xajmi (Tonnada):')
        bot.register_next_step_handler(msg, process_yuk_step)

    except Exception as e:
        bot.reply_to(message, 'ooops!!')

def process_yuk_step(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.yuk_Hajmi = message.text

        msg = bot.send_message(chat_id, 'Xizmat haqi (Dollarda $):')
        bot.register_next_step_handler(msg, process_xizmat_haqi_step)

    except Exception as e:
        bot.reply_to(message, 'ooops!!')

def process_xizmat_haqi_step(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.Xizmat_haqi = message.text

        msg = bot.send_message(chat_id, "Boshlangich to'lov (Dollarda $):")
        bot.register_next_step_handler(msg, process_boshlangich_tulov_step)

    except Exception as e:
        bot.reply_to(message, 'ooops!!')

def process_boshlangich_tulov_step(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.boshlangich_tulov = message.text

        msg = bot.send_message(chat_id, 'Telefon raqamingiz:')
        bot.register_next_step_handler(msg, process_phone_step)

    except Exception as e:
        bot.reply_to(message, 'ooops!!')

def process_phone_step(message):
    try:
        int(message.text)

        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.phone = message.text

        msg = bot.send_message(chat_id, "Qo'shimcha Malumot Yozing:")
        bot.register_next_step_handler(msg, process_qushimcha_malumot_step)

    except Exception as e:
        bot.reply_to(message, 'ooops!!')

def process_qushimcha_malumot_step(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.qushimcha_malumot = message.text

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        itembtn2 = types.KeyboardButton('/elon_berish')
        itembtn1 = types.KeyboardButton('/Biz_haqimizda')
        markup.add(itembtn2, itembtn1)

        # ваша заявка "Имя пользователя"
        bot.send_message(chat_id, getRegData(user, "E'lon Beruvchi: ", message.from_user.first_name), parse_mode="Markdown", reply_markup=markup)
        # отправить в группу
        bot.send_message(config.chat_id, getRegData(user, "E'lon ushbu bot orqali yuborilmoqda: ", bot.get_me().username), parse_mode="Markdown")
        bot.send_message(config.chat_id2, getRegData(user, "E'lon bot orqali yuborilmoqda", bot.get_me().username), parse_mode="Markdown")

    except Exception as e:
        bot.reply_to(message, 'Eloningiz Tayyor!')



# формирует вид заявки регистрации
# нельзя делать перенос строки Template
# в send_message должно стоять parse_mode="Markdown"

def getRegData(user, title, name):
    t = Template(f"$title *$name* \n FISH: *$fullname* \n Qayerdan: *$qayerdan* \n Qayerga: *$qayerga* \n Yuk turi: *$yuk_Turi* \n Yuk hajmi: *$yuk_Hajmi* \n Xizmat haqi: *$Xizmat_haqi*  \n Boshlangich to'lov: *$boshlangich_tulov* \n Telefon raqam: *$phone* \n Qo'shimcha Malumot: *$qushimcha_malumot* ")

    return t.substitute({
        'title': title,
        'name': name,
        'fullname': user.fullname,
        'qayerdan':user.qayerdan,
        'qayerga':user.qayerga,
        'yuk_Turi':user.yuk_Turi,
        'yuk_Hajmi':user.yuk_Hajmi + ' tonna',
        'Xizmat_haqi':user.Xizmat_haqi + ' $',
        'boshlangich_tulov':user.boshlangich_tulov+ ' $',
        'phone': user.phone,
        'qushimcha_malumot':user.qushimcha_malumot,

    })

# произвольный текст
@bot.message_handler(content_types=["text"])
def send_help(message):
    bot.send_message(message.chat.id, "Biz haqimizda - /Biz_haqimizda \nE'lon berish - /elon_berish \nYordam - /help")

# произвольное фото
@bot.message_handler(content_types=["photo"])
def send_help_text(message):
    bot.send_message(message.chat.id, 'Text yozing')

# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

if __name__ == '__main__':
    bot.polling(none_stop=True)
