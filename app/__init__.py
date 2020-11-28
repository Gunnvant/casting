import os
from flask import Flask, jsonify
from .models.models import setup_db
from .auth.auth import AuthError
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    setup_db(app)
    from .routes.routes import routes_blueprint

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,PATCH,DELETE,OPTIONS"
        )
        return response

    app.register_blueprint(routes_blueprint, url_prefix="/api")

    @app.errorhandler(404)
    def not_found(error):
        message = {"success": False, "error": 404, "message": "resource not found"}
        return jsonify(message), 404

    @app.errorhandler(422)
    def unprocessable(error):
        message = {"success": False, "error": 422, "message": "unprocessable entity"}
        return jsonify(message), 422

    @app.errorhandler(405)
    def not_allowed(error):
        message = {"success": False, "error": 405, "message": "method not allowed"}
        return jsonify(message), 405

    @app.errorhandler(400)
    def bad_request(error):
        message = {"success": False, "error": 400, "message": "bad request"}
        return jsonify(message), 400

    @app.errorhandler(401)
    def unauthorized(error):
        message = {"success": False, "error": 401, "message": "unauthorized"}
        return jsonify(message), 401

    @app.errorhandler(AuthError)
    def handle_auth_errors(ex):
        response = jsonify(ex.error)
        response.status_code = ex.status_code
        return response

    return app
