from telebot import TeleBot
from telebot import types

from sqlalchemy         import create_engine
from sqlalchemy         import update
from sqlalchemy         import desc
from sqlalchemy.orm     import sessionmaker
from model import Utente,Points, db_connect, create_table

from settings import *

class Points:    
    def __init__(self):
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def CreateUtente(self, message):
        session = self.Session()
        chatid = message.chat.id
        exist = session.query(Utente).filter_by(id_telegram = chatid).first()  
        if exist is None:
            try:
                utente = Utente()
                utente.username     = '@'+message.chat.username
                utente.nome         = message.chat.first_name
                utente.id_telegram  = message.chat.id
                utente.cognome      = message.chat.last_name
                utente.vita         = 50
                utente.exp          = 0
                utente.livello      = 0
                utente.points       = 0
                utente.premium      = 0
                # logging.info("adding...")
                # logging.info(sell)
                session.add(utente)
                session.commit()
            except:
                session.rollback()
                raise
            finally:
                session.close()
            return False
        return True

    def getUtente(self, target):
        session = self.Session()
        utente = None
        target = str(target)
            
        if target.startswith('@'):
            utente = session.query(Utente).filter_by(username = target).first()
        else:
            chatid = target
            if (chatid.isdigit()):
                chatid = int(chatid)
                utente = session.query(Utente).filter_by(id_telegram = chatid).first()
        return utente


    def update_user(self, chatid, kwargs):
        session = self.Session()
        utente =  session.query(Utente).filter_by(id_telegram=chatid).first()
        for key, value in kwargs.items():  # `kwargs.iteritems()` in Python
            print("updating ",key, "in ",value)
            setattr(utente, key, value) 
        session.commit()
        session.close()

    def addPoints(self, utente, points):  
        chatid = utente.id_telegram  
        punti = int(utente.points) + int(points)
        items = {
            'points': punti
        }    
        self.update_user(chatid,items)

    def donaPoints(self,utenteSorgente,utenteTarget,points):
        points = int(points)
        if points>0:
            if int(utenteSorgente.points)>=points:
                self.addPoints(utenteTarget,points)
                self.addPoints(utenteSorgente,points*-1)
                return utenteSorgente.username+" ha donato "+str(points)+ " "+PointsName+ " a "+utenteTarget.username+ "! ❤️"
            else:
                return PointsName+" non sufficienti"
        else:
            return "Non posso donare "+PointsName+" negativi"


    def buyPremium(self, utente):
        if utente.points>=100:
            items = {
                'points': utente.points-100,
                'premium': 1 
            }
            self.update_user(utente.id_telegram,items)
            return 1
        else:
            return 0
        
        pass

    def buyLowChannel(self, chatid):
        # addpoints(chatid,-15)
        # lista low channel
        pass

    def removePremium(self, chatid):
        # only admin can
        # delete from premium channels
        pass


    def classifica(self):   
        session = self.Session()
        utenti = session.query(Utente).order_by(desc(Utente.livello)).order_by(desc(Utente.exp)).all()
        session.close()
        return utenti
        
    def deleteAccount(self,chatid):
        session = self.Session()
        utente = session.query(Utente).filter_by(id_telegram = chatid).first()  
        session.delete(utente)
        session.commit()


punti = Points()
