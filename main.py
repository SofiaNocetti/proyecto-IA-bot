import telebot
from telebot.types import ReplyKeyboardMarkup
from telebot.types import ForceReply




#conexion
TOKEN=''
bot=telebot.TeleBot(TOKEN)

usuarios={}
#comandos

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'hola! soy turno bot, puedes usar estos comandos para interactuar conmigo,  /alta  ')

@bot.message_handler(commands=['alta'])
def cmd_alta(message):
    markup=ForceReply()
    msg=bot.send_message(message.chat.id, "¿como te llamas?", reply_markup=markup)
    bot.register_next_step_handler(msg, preguntar_edad)

def preguntar_edad(message):
    usuarios[message.chat.id]={'state': 'NAME'}
    usuarios[message.chat.id]["nombres"]=message.text
    markup=ForceReply()
    msg=bot.send_message(message.chat.id, "¿cuantos años tienes?", reply_markup=markup)
    bot.register_next_step_handler(msg, preguntar_sexo)

def preguntar_sexo(message):
    if not message.text.isdigit():
        msg=bot.send_message(message.chat.id, 'Error: debes ingresar un numero.\n ¿cuantos años tienes?')
        bot.register_next_step_handler(msg, preguntar_sexo)
    else:
        usuarios[message.chat.id]["edad"]=int(message.text)
        markup=ReplyKeyboardMarkup(one_time_keyboard=True, input_field_placeholder="pulsa un boton")
        markup.add("hombre","mujer","otro")
        msg=bot.send_message(message.chat.id, '¿cual es tu genero?', reply_markup=markup)


def guardar_datos_usuario(message):
    if message.text !="hombre" and message.text !="mujer" and message.text !="otro":
        msg= bot.send_message(message.chat.id, 'Error: sexo no valido. \n pulsa un boton')
        bot.register_next_step_handler(msg, guardar_datos_usuario)
    else:
        usuarios[message.chat.id]["sexo"]=message.text
    
        


if __name__=="__main__":
    bot.polling(none_stop=True)
