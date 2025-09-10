import os
from flask import Flask, jsonify
from nuskill.auth import auth_bp
from nuskill.tutorials import tuts_bp
from nuskill.payments import payments_bp

def create_app():
    app = Flask(__name__)

    @app.get("/health")
    def health():
        return jsonify(ok=True)

    app.register_blueprint(auth_bp)
    app.register_blueprint(tuts_bp)
    app.register_blueprint(payments_bp)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
