from sqlalchemy import exists

from .db_loader import db_session
from .models import Gender

el1 = Gender(id=0, gender_name="Nope")
el2 = Gender(id=1, gender_name="Female")
el3 = Gender(id=2, gender_name="Male")


def add_gender_info():
    if not db_session.query(exists().where(
            Gender.gender_name == 'Nope'
    )).scalar():

        db_session.add_all([el1, el2, el3])
        db_session.commit()
