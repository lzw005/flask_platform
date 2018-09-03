from flask import Blueprint,jsonify,request
from models import Provinces,Cities,Districts
from webtest import limiter
regions = Blueprint('regions', __name__)

@regions.route('/provinces')
@limiter.exempt
def get_provinces():
    """
    获取provinces
    :return: json
    """
    provinces = Provinces.query.all()
    provinces_dict = {}
    for i in provinces:
        provinces_dict[i.id]=i.name
    return jsonify(provinces_dict)


@regions.route('/cities')
@limiter.exempt
def get_cities():
    """
    根据provinceid获取cities
    :param provinceid: int
    :return: json
    """
    cities_dict = {}
    provinceid=request.args.get("provinceid",None)
    if not provinceid:
        return jsonify(cities_dict)
    province = Provinces.query.filter(Provinces.id == provinceid).first()
    if province:
        for i in province.cities:
            cities_dict[i.id]=i.name
    return jsonify(cities_dict)

@regions.route('/districts')
def get_districts():
    """
    根据cityid获取districts
    :param cityid: int
    :return: json
    """
    districts_dict = {}
    cityid=request.args.get("cityid",None)
    if not cityid:
        return jsonify(districts_dict)
    city = Cities.query.filter(Cities.id == cityid).first()
    if city:
        for i in city.districts:
            districts_dict[i.id]=i.name
    return jsonify(districts_dict)