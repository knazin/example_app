import os
from flask import Flask, render_template, redirect, url_for, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
from flask_sqlalchemy import SQLAlchemy

from app.config import config

app = Flask(__name__)

def update_app(application, config_name):

    # configuration
    app.config.from_object(config[config_name])

    # swagger specific
    SWAGGER_URL = '/api/v1/docs'
    API_URL = '/static/swagger.yaml'
    SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(SWAGGER_URL, API_URL,
        config={ 'app_name': "Python-Flask-REST"}
    )
    application.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

    return application


@app.route('/')
def index():
    return redirect('api/v1/docs')