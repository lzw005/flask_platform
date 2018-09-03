from flask import Blueprint,jsonify,request
import utils

from models import Users
from auths import Auth

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
def register():
    """
    用户注册
    :return: json
    """
    print(request.form)
    return "success"
