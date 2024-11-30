import telebot
from telebot import types
from dotenv import load_dotenv
import os

#conexion
TOKEN='7862828912:AAHM3axnxt7MGWD6kdGgZ9D0aZdJjgxammA'
bot=telebot.TeleBot(TOKEN)

user_data={}

#comandos

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'hola! soy turno bot, Cual es tu nombre?')
    user_data[message.chat.id]={'state' : 'NAME'}

#manejo de nombre

@bot.message_handler(func=lambda  message: user_data.get(message.chat.id, {}).get('state') == "NAME")
def handle_name(message):
    user_data[message.chat.id]['name']=message.text
    user_data[message.chat.id]['state']='SEX'

    #solicitar genero
    markup=types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('hombre',callback_data="sex_masculino"))
    markup.add(types.InlineKeyboardButton('mujer',callback_data="sex_femenino"))
    markup.add(types.InlineKeyboardButton('otro',callback_data="sex_otro"))
    bot.send_message(message.chat.id, "por favor, indica tu genero", reply_markup=markup)

# manejador de genero
@bot.message_handler(func=lambda call:call.data.startswith('sex_'))
def handle_sex(call):
    sex= call.data.split('_')[1]
    user_data[call.message.chat.id]['sex']=sex.capitalize()
    user_data[call.message.chat.id]['state']='TITLE'
    bot.send_message(call.message.chat.id,"cual es el motivo de tu turno?")

#manejador titulo
@bot.message_handler(func=lambda  message: user_data.get(message.chat.id, {}).get('state') == "TITLE")
def handle_title(message):
    user_data[message.chat.id]['title']=message.text
    user_data[message.chat.id]['state']='DESCRIPTION'
    bot.reply_to(message, "por favor, describe tu problema")

@bot.message_handler(func=lambda  message: user_data.get(message.chat.id, {}).get('state') == "DESCRIPTION")
def handle_description(message):
    user_data[message.chat.id]['description'] = message.text
    user_data[message.chat.id]







if __name__=="__main__":
    bot.polling(none_stop=True)