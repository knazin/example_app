from . import api


@api.route("/text", methods=["POST"])
def fetch_text():
    return ""


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
