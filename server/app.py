from AI.main import whichLesson
from loader import db, app
from sqlalchemy.sql import func
from db.models import create_tables, Users, Feedback, Skils, Contibution, Tests, Qessions, Courses
from flask import request,redirect
import random
# from AI.main import whichLesson
import json
import time

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/ai")
def ai():
    req = request.args.get('req').replace('-',' ')
    res = json.dumps(whichLesson(req), ensure_ascii=False)
    time.sleep(3)
    return res

@app.route("/get-tests")
def get_test():
    skill = request.args.get('skill')
    res = {}
    if skill == None:
        tests = Tests.query.all()
    else:
        tests = Tests.query.filter_by(skill=skill).all()
    for test in tests:
        res[test.id] = {"name":test.name,"skill":test.skill}
    return json.dumps(res)

@app.route("/get-questions")
def get_questions():
    test = request.args.get('test')
    quetsions = Qessions.query.filter_by(test_id=test).all()
    res = {}
    for quetsion in quetsions:
        res[quetsion.id] = {"question":quetsion.body,"ansA":quetsion.answerA,"ansB":quetsion.answerB,"ansC":quetsion.answerC,"ansD":quetsion.answerD, "answer":quetsion.answer}
    keys =  list(res.keys())
    random.shuffle(keys)
    resres = {key: res[key] for key in keys}
    return json.dumps(resres)


@app.route("/user/<userid>")
def show_user_profile(userid):
    user = Users.query.filter_by(id=userid).first()
    feed_backs = Feedback.query.filter_by(user_id=user.id).all()
    feed_back_dc = {}
    for feed_back in feed_backs:
        sender_user = Users.query.filter_by(id=feed_back.sender_id).first() 
        if sender_user != None:
            feed_back_dc[feed_back.id] = {"body":feed_back.body, "stars":feed_back.stars, "from_user":sender_user.name}
    contibution = Contibution.query.filter_by(user_id=user.id).all()
    contibution_dc = {}
    for contibut in contibution:
        skill = Skils.query.filter_by(id = contibut.skil_id).first()
        if skill != None:
            contibution_dc[contibut.id] = {'skil_name':skill.skil_name, 'contibution':contibution.contibution}
    return json.dumps({"name":user.name,"about_me":user.about_me,'age':user.age,"feed_back":feed_back_dc, "contibution":contibution_dc, "total_contibution":user.total_contribution, "feedback_count":len(feed_backs)})

@app.route("/TTjrsK0NflCYaMKmc6yZ/addcontibution/<userid>/<skill>/<contibution>")
def add_contibution(userid, skill, contibution):
    skill = Skils.query.filter_by(skil_name=skill).first()
    user = Users.query.filter_by(id = userid).first()
    user.total_contribution += int(contibution)
    contrib = Contibution(user_id = int(userid), skil_id=int(skill.id), contibution = int(contibution))
    db.session.add(contrib)
    db.session.commit()
    return "Successfully added contribution successfully"

@app.route("/TTjrsK0NflCYaMKmc6yZ/create_course")
def create_course():
    contrib = Courses(name = "name")
    db.session.add(contrib)
    db.session.commit()
    return str(contrib.id)

@app.route("/TTjrsK0NflCYaMKmc6yZ/get_user")
def create_course():
    data = {
        'name':"Torossyan David",
        "age":"18",
        "grade":"GameDev Middle",
        "company":"Company: No",
        "contribution":"500",
    }
    return json.dumps(data)

@app.route("/TTjrsK0NflCYaMKmc6yZ/create_course")
def get_articles():
    contrib = Courses(name = "name")
    db.session.add(contrib)
    db.session.commit()
    return str(contrib.id)

@app.route("/TTjrsK0NflCYaMKmc6yZ/logun")
def login():
    #  name = request.args.get('name_and_surname')
    # password = request.args.get('pass')
    #  user = Users(name = name, about_me= about_me, age = int(age), password = password, email = email, grade=grade,company = company)
    return redirect("http://127.0.0.1:5500/client/mainpageauth.html", code=302)

@app.route("/TTjrsK0NflCYaMKmc6yZ/addfeedback/<userto>/<fromuser>/<stars>/<body>")
def add_feedback(userto, fromuser, stars, body):
    feedback = Feedback(user_id = int(userto), sender_id=int(fromuser), stars = int(stars), body = body)
    db.session.add(feedback)
    db.session.commit()
    return "Feedback successfully received"

@app.route("/TTjrsK0NflCYaMKmc6yZ/register/")
def register_user():
    name = request.args.get('name_and_surname')
    about_me = request.args.get('about_me')
    grade = request.args.get('grade')
    age = int(request.args.get('age'))
    password = request.args.get('pass')
    email = request.args.get('email')
    skills = request.args.get('skills')
    company = request.args.get('company')

    user = Users(name = name, about_me= about_me, age = int(age), password = password, email = email, grade=grade,company = company)
    db.session.add(user)
    db.session.commit()
    if skills != None:
        skills_array = skills.split("|")
        for skill in skills_array:
            skill = Skils(user_id = user.id, skil_name = skill)
            db.session.add(skill)
            db.session.commit()
    return redirect("http://127.0.0.1:5500/client/mainpageauth.html", code=302)

@app.route("/TTjrsK0NflCYaMKmc6yZ/get_user_from_skill/<skilname>")
def get_user_from_skill(skilname):
    res = {}
    skill_array = skilname.split("|")
    for skill_name in skill_array:
        skills = Skils.query.filter_by(skil_name = skill_name).all()
        for skill in skills:
            user = Users.query.filter_by(id = skill.user_id).first()
            res[user.id] = user.name
    return json.dumps(res)

@app.route("/gettopcontribution")
def get_top_contribution():#сор
    users = Users.query.order_by(Users.total_contribution.desc()).all()
    raiting = {}
    for user in users:
        skils = Skils.query.filter_by(user_id = user.id).all()
        if skils == None:
            skils_str = ""
        else:
            skill_names = [skill.skil_name for skill in skils]
            skils_str= ', '.join(skill_names)
        
        raiting[user.id] = {"name":user.name, "about":user.about_me, "total_contribution":user.total_contribution, "email":user.email, 'skills':skils_str}
    return json.dumps(raiting)

with app.app_context():
    create_tables()

if __name__ == '__main__':
    app.run()