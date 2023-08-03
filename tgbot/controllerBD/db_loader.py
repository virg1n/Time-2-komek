from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, Session
import sqlite3
conn = sqlite3.connect('C:/Users/User/Desktop/Programming/Data/fizmathck/tgbot/data/coffee_database.db')

engine = create_engine('sqlite:///C:/Users/User/Desktop/Programming/Data/fizmathck/tgbot/data/coffee_database.db')
engine.connect()
db_session = Session(bind=engine)

Base = declarative_base()
