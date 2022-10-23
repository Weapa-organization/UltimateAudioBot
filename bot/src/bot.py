import telebot
import logging as log
import signal
import time
import sys
import os

from enum import Enum

from SoundManager import SoundManager as sm
from ConectApi import ConectApi as ca

bot = telebot.TeleBot(os.environ.get('BOT_TOKEN'), parse_mode=None)


class filters(Enum):
    reverse = "reverse"
    distorsio = "distorsio"
    loop = "loop"
    eco = "eco"
    reverberation = "reverberation"


@bot.message_handler(commands=['start', 'help'])
def welcome_message(message):
    msg = "Este bot esta de prueba, no se que mas decir"
    bot.send_message(message.chat.id, msg)


@bot.message_handler(commands=['mis_datos'])
def mis_datos(message):
    msg = "los datos del usuario son: " + "\n"
    msg += "Nombre: " + str(message.from_user.first_name)+ "\n"
    msg += "Apellido: " + str(message.from_user.last_name)+ "\n"
    msg += "Username: " + str(message.from_user.username) + "\n"
    msg += "Id: " + str(message.from_user.id) + "\n"
    msg += "grupo: " + str(message.chat.id) + "\n"
    msg += "tipo de grupo: " + str(message.chat.type) + "\n"
    msg += "titulo del grupo: " + str(message.chat.title) + "\n"
    msg += "descripcion del grupo: " + str(message.chat.description) + "\n"
    msg += "link del grupo: " + str(message.chat.invite_link) + "\n"
    bot.send_message(message.chat.id, msg)


@bot.message_handler(commands=['reverse', 'eco', 'distorsio', 'reverberation'])
def select_filter(message):
    filter = message.text[1:]
    # bot.send_message(message.chat.id, "El filtro seleccionado es: " + filter)
    if filter == filters.reverse.value:
        ca.update_state(message.from_user.id, message.from_user.username, filters.reverse.value)
        # bot.send_message(message.chat.id, "reverse")
    elif filter == filters.eco.value:
        ca.update_state(message.from_user.id, message.from_user.username, filters.eco.value)
        # bot.send_message(message.chat.id, "eco")
    elif filter == filters.distorsio.value:
        ca.update_state(message.from_user.id, message.from_user.username, filters.distorsio.value)
        # bot.send_message(message.chat.id, "distorsio")
    elif filter == filters.reverberation.value:
        ca.update_state(message.from_user.id, message.from_user.username, filters.reverberation.value)


@bot.message_handler(commands=['filter'])
def get_filter(message):
    filter = ca.get_state(message.from_user.id, message.from_user.username)
    bot.send_message(message.chat.id, "El filtro seleccionado es: " + filter)


@bot.message_handler(content_types=['video_note', 'voice'])
def send_voice(message):

    file_info = bot.get_file(message.voice.file_id)
    # log.info(message.id)

    # Descargar y guardar el archivo de audio
    downloaded_file = bot.download_file(file_info.file_path)
    src =  os.path.join(os.getcwd(), 'audios', file_info.file_path)
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)

    # Aplicar el filtro
    filter_state = ca.get_state(message.from_user.id, message.from_user.username)
    if filter_state == filters.reverse.value:
        bot.send_voice(message.chat.id, sm.reverse_sound(src),None,message.voice.duration,message.id)
    elif filter_state == filters.eco.value:
        bot.send_voice(message.chat.id, sm.eco_sound(src),None,message.voice.duration,message.id)
    elif filter_state == filters.distorsio.value:
        bot.send_voice(message.chat.id, sm.distorsio_sound(src),None,message.voice.duration,message.id)
    elif filter_state == filters.reverberation.value:
        bot.send_voice(message.chat.id, sm.reverberation_sound(src),None,message.voice.duration,message.id)

    # bot.reply_backend

    # remove the audio file
    os.remove(src)


def main():
    log.basicConfig(level=log.INFO,format='%(asctime)s %(levelname)s %(message)s')
    signal.signal(signal.SIGINT, signal_handler)

    while True:
        try:
            log.info('Starting bot polling...')
            bot.polling()
        except Exception as err:
            log.error("Bot polling error: {0}".format(err.args))
            bot.stop_polling()
            time.sleep(30)


def signal_handler(signal_number, frame):
    print('Received signal ' + str(signal_number)
          + '. Trying to end tasks and exit...')
    bot.stop_polling()
    sys.exit(0)

if __name__ == "__main__":
    main()