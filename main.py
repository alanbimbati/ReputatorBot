from telebot import types
from telebot import TeleBot
from settings import *
from sqlalchemy         import create_engine
from sqlalchemy.orm     import sessionmaker

from model import Utente,Points, db_connect, create_table
import Points
from telebot import util

bot = TeleBot(BOT_TOKEN, threaded=False)


hideBoard = types.ReplyKeyboardRemove()  


@bot.message_handler(commands=['start'])
def start(message):
    punti = Points.Points()
    if message.chat.type == "private":
        
        alreadyExist = punti.CreateUtente(message)
        if alreadyExist == False:
            bot.send_message(message.chat.id, 'Benvenuto su aROMa!')
        else:
            bot.send_message(message.chat.id, 'io ti ho già visto...')

@bot.message_handler(content_types=util.content_type_media)
def any(message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        chatid = message.from_user.id
    elif message.chat.type == 'private':
        chatid = message.chat.id
        if message.text.lower() == 'backup':
            doc = open('points.db', 'rb')
            bot.send_document(message.chat.id, doc, caption="aROMa #database #backup")
            doc.close()

    punti = Points.Points()

    points,target = givePoints(message)
    utenteSorgente  = punti.getUtente(chatid)
    utenteTarget    = punti.getUtente(target)  

    # ADMINistrazione dei punti
    for admin in ADMIN:
        if str(chatid) == str(ADMIN[admin]):
            if message.text[0]=='+' or message.text[0]=='-':
                if utenteTarget is None:
                    bot.reply_to(message, "L'utente "+target+" deve avviarmi in privato (@aROMaGameBot)")
                else:
                    if message.text[0]=='+':
                        punti.addPoints(utenteTarget, points)
                        bot.reply_to(message, "Complimenti! Hai ottenuto "+ points +' '+PointsName)
                    elif message.text[0]=='-':
                        punti.addPoints(utenteTarget, int(points)*-1)       
                        bot.reply_to(message, "Hai mangiato "+points+' '+PointsName)

    if message.text.startswith('dona'):
        if utenteTarget is None:
            bot.reply_to(message, "L'utente "+target+" deve avviarmi in privato (@aROMaGameBot)")
        else:
            messaggio = punti.donaPoints(utenteSorgente,utenteTarget,points)
            bot.reply_to(message,messaggio)
    elif message.text == '!me' or message.text == '/me':
        if utenteSorgente is None:
            bot.reply_to(message, "L'utente "+utenteSorgente.nome+" deve avviarmi in privato (@aROMaGameBot)")
        else:
            bot.reply_to(message, utenteSorgente.nome+": "+str(utenteSorgente.points)+" "+PointsName)
    #elif message.text == "!earn" or  message.text == '/me':
     #   bot.reply_to(message, EARN, parse_mode='HTML')

def givePoints(message):
    msg = []
    if message.text[0]=='+' or message.text[0]=='-':
        msg = message.text[1:].split()
    elif message.text.startswith('dona'):
        msg = message.text[4:].split()

    points = 0
    target = ''
    if len(msg)>=1:
        points = str(msg[0])
    if len(msg)>=2:
        target = str(msg[1])
    return points,target

bot.infinity_polling()

