import datetime,re
from exts import db
from sqlalchemy.exc import SQLAlchemyError



class Users(db.Model):
    __tablename__ = 'wushu_users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30),  unique=True, nullable=False)
    name = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    duty = db.Column(db.String(20), nullable=False)
    telephone = db.Column(db.String(20), nullable=False)
    mobile_phone = db.Column(db.String(20), nullable=False)
    school_name = db.Column(db.String(30), nullable=False)
    school_type = db.Column(db.String(20), nullable=False)
    identification_type = db.Column(db.String(20), nullable=False)
    identification_num = db.Column(db.String(30), nullable=False)
    provinceid = db.Column(db.Integer)
    cityid = db.Column(db.Integer)
    districtid = db.Column(db.Integer)
    remark = db.Column(db.String(300))

    login_time = db.Column(db.Integer)
    email_confirmed = db.Column(db.Boolean)

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

    @property
    def is_email_confirmed(self):
        """Return True if the user confirmed their email address."""
        return self.email_confirmed

    def validate_email(self, email):
        if not re.match(r'^[0-9a-zA-Z\_]+@[0-9a-zA-Z\.]+$',email):
            return False,'邮箱有误'
        if Users.query.filter_by(email=email).first():
            return False,'邮箱已被注册'
        return True,'邮箱有效'


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

