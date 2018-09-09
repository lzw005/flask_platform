from flask import Blueprint,jsonify,request
from models import Teams,Users
from auths import Auth
from exts import db
from sqlalchemy.exc import SQLAlchemyError
import utils
teams = Blueprint('teams', __name__)

@teams.route('/teams',methods=["GET",'POST'])
def team():
    response = Auth.identify(Auth, request)
    if (response['status'] and response['data']):
        user = Users.get(Users, response['data']['id'])
        returnUser = {
            'id': user.id,
            'username': user.name,
            'email': user.email,
            'login_time': user.login_time
        }
        return jsonify(utils.success_response('请求成功',returnUser))
    return jsonify(response)

    if request.method == 'POST':
        print(request.form)
        team = Teams(name = request.form.get('teamname'),
                     short_name = request.form.get('shortname'),
                     en_name = request.form.get('englishname'),
                     state = request.form.get('state'),
                     countryid = request.form.get('country'),
                     provinceid = request.form.get('province'),
                     cityid = request.form.get('city'),
                     districtid = request.form.get('district'),
                     detail_address = request.form.get('detailaddress'),
                     pname = request.form.get('pname'),
                     pwx = request.form.get('pwx'),
                     ptelephone = request.form.get('ptelephone'),
                     pemail = request.form.get('pemail'))
        try:
            db.session.add(team)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            reason = str(e)
            return utils.error_response(reason)

    if request.method == 'GET':


        return 'success'
    return 'success'