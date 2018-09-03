#encoding:utf-8
from flask import Flask,render_template,request, jsonify
import os
from flask_cors import *
from flask_mail import Mail
from flask_script import Manager,Server
from flask_migrate import Migrate, MigrateCommand
import utils
from exts import db
from models import Users
from auths import Auth
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


app = Flask(__name__)



app.config.from_object("settings.Config")
db.init_app(app)

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command("runserver", Server(host = '0.0.0.0'))

limiter = Limiter(
    app,
    key_func=get_remote_address,   #根据访问者的IP记录访问次数
    default_limits=["200 per day", "50 per hour"]  #默认限制，一天最多访问200次，一小时最多访问50次
)


mail = Mail(app)

CORS(app, supports_credentials=True)        #跨域请求

basedir = os.path.abspath(os.path.dirname(__file__))

from views.regions import regions as regions_blueprint
from views.teams import teams as teams_blueprint
app.register_blueprint(regions_blueprint)
app.register_blueprint(teams_blueprint)



@app.route('/up', methods = ['POST','GET'])
def up_photo():
    if request.method =="POST":

        print(request.files)
        img = request.files.get('photo')
        path = basedir+"/static/"
        file_path = path+img.filename
        print(file_path)
        img.save(file_path)
        print ('上传头像成功，'+img.filename)
        return "success"
    else:
        return render_template('image.html')

@app.route('/login', methods=['POST'])
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

@app.route('/register', methods=['POST'])
def register():
    """
    用户注册
    :return: json
    """
    print(request.form)
    return "success"




@app.route('/users/confirm')
@limiter.limit("2 per minute")
def confirm_email():
    """
    获取用户信息
    :return: json
    """
    email = request.args.get("email", None)
    print(email)
    # utils.send_confirmation_email('1372241206@qq.com')

    return '<h1>邮件发送成功</h1>'


@app.route('/user', methods=['GET'])
def get():
    """
    获取用户信息
    :return: json
    """
    response = Auth.identify(Auth, request)
    if (response['status'] and response['data']):
        user = Users.get(Users, response['data']['id'])
        returnUser = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'login_time': user.login_time
        }
        return jsonify(utils.success_response('请求成功',returnUser))
    return jsonify(response)



if __name__ == '__main__':
    app.run(host='0.0.0.0')
    # manager.run()