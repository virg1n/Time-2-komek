from loader import db

class Contibution(db.Model):
    __tablename__ = 'contibution'
    id = db.Column(db.Integer, primary_key=True, nullable=False,
                unique=True, autoincrement=True)
    user_id = db.Column(db.ForeignKey("users.id", ondelete="CASCADE"))
    skil_id = db.Column(db.ForeignKey("skils.id", ondelete="CASCADE"))
    contibution = db.Column(db.Integer, nullable=False, default=0)

class SkilsList(db.Model):
    __tablename__ = 'skils'
    id = db.Column(db.Integer, primary_key=True, nullable=False,
                unique=True, autoincrement=True)
    skil_name = db.Column(db.String, nullable=False)
    
class Skils(db.Model):
    __tablename__ = 'user_skils'
    id = db.Column(db.Integer, primary_key=True, nullable=False,
                unique=True, autoincrement=True)
    user_id = db.Column(db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    skil_name = db.Column(db.ForeignKey("skils.id", ondelete="CASCADE"), nullable=False)
    user = db.relationship("Users", back_populates="skils")

class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True, nullable=False,
                   unique=True, autoincrement=True)
    user_id = db.Column(db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    sender_id = db.Column(db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    stars = db.Column(db.Integer, nullable=False, default=0)
    body = db.Column(db.String, nullable=False)
    ordered_product = db.relationship("Users", foreign_keys=[user_id], back_populates="feedback_received")
    ordered_by = db.relationship("Users", foreign_keys=[sender_id], back_populates="feedback_sent")

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, nullable=False,
                unique=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    about_me = db.Column(db.String)
    age = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String, nullable=False)
    grade = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    company = db.Column(db.String, nullable=False)
    total_contribution = db.Column(db.Integer, nullable=False, default=0)
    skils = db.relationship("Skils", back_populates="user")
    feedback_received = db.relationship('Feedback', foreign_keys=[Feedback.user_id], backref='user')
    feedback_sent = db.relationship('Feedback', foreign_keys=[Feedback.sender_id], backref='feedback_sent_by')

class Tests(db.Model):
    __tablename__ = 'tests'
    id = db.Column(db.Integer, primary_key=True, nullable=False,
                unique=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    skill = db.Column(db.String, nullable=False)
    admin = db.Column(db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

class Qessions(db.Model):
    __tablename__ = 'quessions'
    id = db.Column(db.Integer, primary_key=True, nullable=False,
                unique=True, autoincrement=True)
    test_id = db.Column(db.ForeignKey("tests.id", ondelete="CASCADE"), nullable=False)
    body = db.Column(db.String, nullable=False)
    answerA = db.Column(db.String, nullable=False)
    answerB = db.Column(db.String, nullable=False)
    answerC = db.Column(db.String, nullable=False)
    answerD = db.Column(db.String, nullable=False)


class Courses(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True, nullable=False,
                unique=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    

class Articles(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True, nullable=False,
                unique=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    body = db.Column(db.String, nullable=False)
    tutorial = db.Column(db.ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)

def create_tables():
    db.create_all()