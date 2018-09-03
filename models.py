import datetime
from exts import db
from sqlalchemy.exc import SQLAlchemyError


class Users(db.Model):
    __tablename__ = 'wushu_users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250),  unique=True, nullable=False)
    username = db.Column(db.String(250),  unique=True, nullable=False)
    password = db.Column(db.String(250))
    login_time = db.Column(db.Integer)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    def __str__(self):
        return "Users(id='%s')" % self.id

    # def set_password(self, password):
    #     return generate_password_hash(password)
    #
    def check_password(self, real_pw, input_pw):
        if real_pw == input_pw:
            return True
        return False

    def get(self, id):
        return self.query.filter_by(id=id).first()

    def add(self, user):
        db.session.add(user)
        return session_commit()

    def update(self):
        return session_commit()

    def delete(self, id):
        self.query.filter_by(id=id).delete()
        return session_commit()


def session_commit():
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        reason = str(e)
        return reason

class Teams(db.Model):
    __tablename__ = 'wushu_teams'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20), nullable = False)
    short_name = db.Column(db.String(20), nullable = False)
    en_name = db.Column(db.String(20), nullable = False)
    state = db.Column(db.String(20), nullable = False)
    countryid = db.Column(db.String(20), nullable = False)
    provinceid = db.Column(db.String(20), nullable = False)
    cityid = db.Column(db.String(20), nullable = False)
    detail_address = db.Column(db.String(40), nullable = False)

    pid = db.Column(db.Integer, nullable = False)
    pname = db.Column(db.String(20), nullable = False)
    pwx = db.Column(db.String(30), nullable = False)
    ptelephone = db.Column(db.String(20), nullable = False)
    pemail = db.Column(db.String(20), nullable = False)
    date_posted = db.Column(db.DateTime, nullable = False)
    def __init__(self, text):
        self.date_posted = datetime.datetime.now()

class Provinces(db.Model):
    __tablename__ = 'wushu_provinces'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(10), nullable = False)
    countryid = db.Column(db.Integer, nullable = False)
    canDelete = db.Column(db.Boolean)
    cities = db.relationship('Cities', backref = 'province')



class Cities(db.Model):
    __tablename__ = 'wushu_cities'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20), nullable = False)
    provinceid = db.Column(db.Integer, db.ForeignKey('wushu_provinces.id'))
    canDelete = db.Column(db.Boolean)
    districts = db.relationship('Districts', backref = 'city')


class Districts(db.Model):
    __tablename__ = 'wushu_districts'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20), nullable = False)
    cityid = db.Column(db.Integer, db.ForeignKey('wushu_cities.id'))
    canDelete = db.Column(db.Boolean)

