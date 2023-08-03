from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, Session

DATABASE_URL = 'postgresql://postgres:1q2w3e4r@localhost:5432/ter_hak'

engine = create_engine(DATABASE_URL)
engine.connect()
db_session = Session(bind=engine)

Base = declarative_base()