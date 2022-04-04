from ast import Str
from sqlalchemy                 import create_engine, Column, Table, ForeignKey, MetaData
from sqlalchemy.orm             import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy                 import (Integer, String, Date, DateTime, Float, Boolean, Text)

Base = declarative_base()


def db_connect():
    return create_engine('sqlite:///points.db')
    
def create_table(engine):
    Base.metadata.create_all(engine)

class Utente(Base):
    __tablename__ = "utente"
    id = Column(Integer, primary_key=True)
    id_telegram = Column('id_Telegram', Integer, unique=True)
    nome  = Column('nome', String(32))
    cognome = Column('cognome', String(32))
    username = Column('username', String(32), unique=True)
    exp = Column('exp', Integer)
    points = Column('money', Integer)
    livello = Column('livello', Integer)
    vita = Column('vita', Integer)
    premium = Column('premium', Integer)

class Points(Base):
    __tablename__ = "points"
    id = Column(Integer, primary_key=True)
    numero = Column('numero', Integer)
    gruppo = Column(Integer,) 
    nome = Column('nome',String(64))
