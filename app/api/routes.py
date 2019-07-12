from flask import request
from . import api
from .models import Text
from .methods import (
    run_fetch_task
)


@api.route("/text", methods=["POST"])
def fetch_text():
    url = request.json["url"]
    text = Text.query.filter_by(url=url).first()

    return run_fetch_task(text, 'get_text', url)


@api.route("/images", methods=["POST"])
def fetch_images():
    return ""


@api.route("/text", methods=["GET"])
def download_text():
    return ""


@api.route("/images", methods=["GET"])
def download_images():
    return ""


@api.route("/task/<string:task_id>", methods=["GET"])
def check_task(task_id):
    return ""
