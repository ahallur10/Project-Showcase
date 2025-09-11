import json
from flask import Blueprint, request
from snowflake_db.snowflake_engine import get_user,get_user_balance
from payment.payment_services import make_deposit
from payment.coinbase import requestFundsFromUser
payment_services_handler = Blueprint('payment_services_handler', __name__, template_folder='templates')


@payment_services_handler.route('/payment/deposit', methods=['POST'])
def deposit():
    data = request.get_json()
    make_deposit(data['id'],data['amount'])
    redirect_url = requestFundsFromUser(data['amount'])
    return {'status':200, 'body': redirect_url}

@payment_services_handler.route("/payment/current_balance", methods=['POST'])
def get_current_balance():
    data = request.get_json()

    return {'status':200, 'body': get_user_balance(data['user_id'])}



@payment_services_handler.route('/payment/withdraw')
def withdraw():
    return ''
