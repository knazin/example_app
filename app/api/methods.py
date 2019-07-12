import os, sys, inspect

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from api.models import Text, Image
from api.worker import celery

from flask import session, jsonify, url_for, send_file

import lxml
import requests
import celery.states as states
from lxml.html import fromstring, HtmlElement

import zipfile
from io import BytesIO
from zipfile import ZipFile
from flask import session, jsonify, url_for, send_file


def set_message_and_state(res):
    
    message = ""
    state = res.state

    if res.state == "SUCCESS":
        message = res.result

        if "ERROR" in message:
            state = "ERROR"
        else:
            state == "SUCCESS"

    elif res.state == "PENDING":
        state = "PENDING"

    return (message, state)


def extract_text_from_html(url):
    r = requests.get(url)
    r.encoding = "utf-8"
    html = fromstring(r.text)

    text = ""
    for d in html.iterdescendants():
        if d.tag not in ["script", "style"] and type(d) == HtmlElement:
            try:
                text += d.text + " "
            except:
                pass

    text = text.replace("  ", "").replace("\n\n", "").replace("\t", "")

    return text


def name_from_image_attributes(image_attributes, nr, image_ext):
    
    if 'title' in image_attributes and image_attributes['title'] != '':
        image_name = image_attributes['title']
    elif 'alt' in image_attributes and image_attributes['alt'] != '':
        image_name = image_attributes['alt']
    else:
        image_name = f'image_{nr}'

    image_name = image_name.replace('/','') + f'.{image_ext}'

    return image_name


def pack_images_to_zipfile(images):
    
    file = BytesIO()
    
    with zipfile.ZipFile(file, 'w') as zf:
        
        for image in images:
            data = zipfile.ZipInfo(image.name)
            data.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(data, image.data)
    
    file.seek(0)

    return file


def run_fetch_task(item, task_name, url):

    if not item:
        task = celery.send_task(task_name, args=[url], kwargs={})

        return (
            jsonify({
                "task_id": str(task.id),
                "check_task_status": f"{url_for('api.check_task', task_id=task.id, external=True)}",
            }), 202,
        )

    message = "Images" if "text" in task_name else "Text"
    message += " from this website is already downloaded."

    return jsonify({"url": url, "message": message}), 206


def downloaded_data(data_in_db, url, data_type):
    
    if not data_in_db:
        return jsonify({
            "url": url,
            "message": "No images for this url" if data_type == 'images' else "No text for this url"
        }), 206

    elif data_type == 'images':
        
        zipped_images = pack_images_to_zipfile(data_in_db)
        return send_file(zipped_images, attachment_filename='images.zip', as_attachment=True), 200

    elif data_type == 'text':
            return jsonify({
            "task_id": data_in_db.task_id,
            "url": url,
            "text_from_website": data_in_db.text,
        }), 200