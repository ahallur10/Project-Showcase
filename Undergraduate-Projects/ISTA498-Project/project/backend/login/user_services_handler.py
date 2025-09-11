import json
from flask import Blueprint, request
from login.register import sign_up, id_login
from snowflake_db.snowflake_engine import get_user,get_user_deposited
user_services_handler = Blueprint('user_services_handler', __name__, template_folder='templates')


@user_services_handler.route("/user/register", methods=['POST'])
def register():
    data = request.get_json()
    if len(get_user(data['user_id'])) == 0:
        sign_up(data['user_id'], data['password'])
        return {'status': 200, 'body': 'Success'}
    else:
        return {'status': 200, 'body': 'ID already registered'}

@user_services_handler.route("/user/login", methods=['POST'])
def login():
    data = request.get_json()
    id_login(data['user_id'], data['password'])    
    return {'status': 200, 'body': 'Success'}

@user_services_handler.route("/user/status", methods=['POST'])
def status():
    data = request.get_json()
    return {'status':200, 'body': get_user_deposited(data['user_id'])}