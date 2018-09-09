import os
from datetime import timedelta

class Config(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://Ubuntu:123456@106.14.140.30:3306/wushu'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'asajsfa1o3mfp1p3kpwofkwpkfpewkeopskpda'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=3)  # 配置过期时间

    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = 'zyh_shdx@163.com'
    MAIL_PASSWORD = 'zyh19980310'
    MAIL_DEFAULT_SENDER = 'zyh_shdx@163.com'
