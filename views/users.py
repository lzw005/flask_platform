from flask import Blueprint,jsonify,request
import utils
from exts import db
from sqlalchemy.exc import SQLAlchemyError
from itsdangerous import URLSafeTimedSerializer
from models import Users
from auths import Auth
from webtest import limiter

users = Blueprint('users', __name__)

@users.route('/login', methods=['POST'])
def login():
    """
    用户登录
    :return: json
    """
    username = request.form.get('username')
    password = request.form.get('password')
    if not username or not password:
        return jsonify(utils.error_response("用户名或密码不能为空"))
    else:
        return jsonify(Auth.authenticate(Auth, username, password))

@users.route('/register', methods=['POST'])
@limiter.limit("100 per hour")
def register():
    """
    用户注册
    :return: json
    """
    validate_email = Users.validate_email(Users,request.form.get('email'))
    if not validate_email[0]:
        return jsonify(utils.error_response(validate_email[1]))
    user = Users(name = request.form.get('name'),
                 email = validate_email[1],
                 password = request.form.get('password'),
                 duty = request.form.get('duty'),
                 telephone = request.form.get('telephone'),
                 mobile_phone = request.form.get('mobile_phone'),
                 school_name = request.form.get('school_name'),
                 school_type = request.form.get('school_type'),
                 identification_num = request.form.get('identification_num'),
                 identification_type = request.form.get('identification_type'),
                 provinceid = int(request.form.get('province',310000)),
                 cityid = int(request.form.get('city',310100)),
                 districtid = int(request.form.get('district',310101)),
                 remark = request.form.get('remark'),
                 email_confirmed = False)
    try:
        db.session.add(user)
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        reason = str(e)
        return utils.error_response(reason)
    utils.send_confirmation_email(validate_email[1])
    return jsonify(utils.success_response('注册成功',user.email))


@users.route('/confirm/<token>')
def confirm_email(token):
    try:
        confirm_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        email = confirm_serializer.loads(token, salt='email-confirmation-salt', max_age=3600)
    except:
        # message = Markup(
        #     "The confirmation link is invalid or has expired.")
        # flash(message, 'danger')
        return "连接失效"

    user = Users.query.filter_by(email=email).first()

    if user.email_confirmed:
        # message = Markup(
        #     "Account already confirmed. Please login.")
        # flash(message, 'info')
        return "已确认，请登陆"
    else:
        user.email_confirmed = True
        db.session.add(user)
        db.session.commit()
        # message = Markup(
        #     "Thank you for confirming your email address!")
        # flash(message, 'success')
    return '确认成功'