from webtest import mail
from flask_mail import Message
from threading import Thread
from flask import url_for,render_template
from itsdangerous import URLSafeTimedSerializer
from settings import Config as config
from webtest import app
def send_async_email(msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, recipients, html_body):
    '''
    :param subject: 标题
    :param recipients: 收件人
    :param html_body: 确认网页
    :return:
    '''
    msg = Message(subject,recipients=recipients)
    msg.html = html_body
    thr = Thread(target=send_async_email, args=[msg])
    thr.start()

def send_confirmation_email(user_email):
    '''
    :param user_email: 收件人
    :return:
    '''
    confirm_serializer = URLSafeTimedSerializer(config.SECRET_KEY)

    confirm_url = url_for(
        'users.confirm_email',
        token = confirm_serializer.dumps(user_email, salt='email-confirmation-salt'),
        _external=True)
    print("url:",confirm_url)

    html = render_template(
        'email_confirmation.html',
        confirm_url=confirm_url)

    send_email('Confirm Your Email Address', [user_email], html)

def send_password_reset_email(user_email):
    password_reset_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

    password_reset_url = url_for(
        'users.reset_with_token',
        token=password_reset_serializer.dumps(user_email, salt='password-reset-salt'),
        _external=True)

    html = render_template(
        'email_password_reset.html',
        password_reset_url=password_reset_url)

    send_email('Password Reset Requested', [user_email], html)

def error_response(msg,data = None):
    if data is None:
        data={}
    temp = {'status':False,'msg':msg,'data':data}
    return temp

def success_response(msg,data = None):
    if data is None:
        data={}
    temp = {'status':True,'msg':msg,'data':data}
    return temp


# from functools import wraps
# from flask import make_response


# def allow_cross_domain(fun):
#     @wraps(fun)
#     def wrapper_fun(*args, **kwargs):
#         rst = make_response(fun(*args, **kwargs))
#         rst.headers['Access-Control-Allow-Origin'] = '*'
#         rst.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
#         allow_headers = "Referer,Accept,Origin,User-Agent"
#         rst.headers['Access-Control-Allow-Headers'] = allow_headers
#         return rst
#     return wrapper_fun

# def Verifi_code_mail():
#     return ''.join([random.choice(string.ascii_uppercase+string.digits) for i in range(6)])