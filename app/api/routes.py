from flask import request, jsonify
from . import api
from .models import Text, Image
from .worker import celery
from .methods import run_fetch_task, set_message_and_state, downloaded_data


@api.route("/text", methods=["POST"])
def fetch_text():
    url = request.json["url"]
    text = Text.query.filter_by(url=url).first()

    return run_fetch_task(text, "get_text", url)


@api.route("/images", methods=["POST"])
def fetch_images():
    url = request.json["url"]
    images = Image.query.filter_by(url=url).all()

    return run_fetch_task(images, 'get_images', url)


@api.route("/text", methods=["GET"])
def download_text():
    url = request.json["url"]
    text = Text.query.filter_by(url=url).first()

    return downloaded_data(text, url, 'text')


@api.route("/images", methods=["GET"])
def download_images():
    return ""


@api.route("/task/<string:task_id>", methods=["GET"])
def check_task(task_id):
    res = celery.AsyncResult(task_id)
    message, state = set_message_and_state(res)

    return jsonify({"task_id": task_id, "state": state, "message": message}), 200
