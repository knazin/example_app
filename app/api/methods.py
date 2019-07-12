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


def extract_text_from_html(url):
    r = requests.get(url)
    r.encoding = 'utf-8'
    html = fromstring(r.text)

    text = ''
    for d in html.iterdescendants():
        if d.tag not in ['script','style'] and type(d) == HtmlElement:
            try: text += d.text + ' '
            except: pass
            
    text = text.replace('  ','').replace('\n\n','').replace('\t','')

    return text


def run_fetch_task(item, task_name, url):
    
    if not item:
        task = celery.send_task(task_name, args=[url], kwargs={})

        return jsonify({
            "task_id": str(task.id),
            "check_task_status": f"{url_for('api.check_task', task_id=task.id, external=True)}"
        }), 202

    message = "Images" if "text" in task_name else "Text"
    message += " from this website is already downloaded."

    return jsonify({
        "url": url,
        "message": message
    }), 206