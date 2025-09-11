from flask import Blueprint, request

from snowflake_db.snowflake_engine import get_genre_map
tutorial_services_handler = Blueprint('tutorial_services_handler', __name__, template_folder='templates')


@tutorial_services_handler.route("/tutorial/videos", methods=['GET'])
def get_current_balance():
    return {'status':200, 'body': get_genre_map()}

