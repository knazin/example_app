import os
from flask import Flask, render_template, redirect, url_for, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
from flask_sqlalchemy import SQLAlchemy

from app.config import config

app = Flask(__name__)

def update_app(application, config_name):

    # configuration
    app.config.from_object(config[config_name])

    return application


@app.route('/')
def index():
    return "Hello"