import os
from datetime import timedelta

class Config(object):
    DEBUG=True
    SQLALCHEMY_DATABASE_URI = ''
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = ''
    PERMANENT_SESSION_LIFETIME = timedelta(hours=3)  # 配置过期时间

    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = ''
    MAIL_PASSWORD = ''
    MAIL_DEFAULT_SENDER = ''
