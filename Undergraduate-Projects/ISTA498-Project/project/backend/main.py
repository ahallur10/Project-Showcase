from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os
from payment.payment_services_handler import payment_services_handler
from login.user_services_handler import user_services_handler
from tutorial.tutorial_services_handler import tutorial_services_handler
load_dotenv()

app = Flask(__name__)
# to-do later: add only frontend domain to access
CORS(app)

app.register_blueprint(user_services_handler)
app.register_blueprint(payment_services_handler)
app.register_blueprint(tutorial_services_handler)


@app.route("/")
def weclome():
    return f"Welcome to NuSkill API"

if __name__ == "__main__":
    app.run(debug=True,port=os.environ.get('PORT'))