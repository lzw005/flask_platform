from flask import Blueprint,jsonify,request
from models import Teams

teams = Blueprint('teams', __name__)

@teams.route('/teams',methods=["GET",'POST'])
def team():
    print(request.form)
    return 'success'