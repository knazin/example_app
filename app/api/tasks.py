import os, sys, inspect

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import os
import time
import base64
import requests
from lxml.html import fromstring
from celery import Celery
import sqlalchemy
from sqlalchemy.orm import sessionmaker
import validators

from models import Text, Image
from methods import extract_text_from_html

from dotenv import load_dotenv

load_dotenv(dotenv_path="../.env")

# START
# celery -A tasks worker --loglevel=info

### ENVIRONMENT/GLOBAL VARIABLES ###

STATE = os.environ["CONFIG_TYPE"]

if STATE == "development":
    DB_URI_WORKER = os.environ["DEV_DATABASE_URI_WORKER"]
    CELERY_BROKER_URL = os.environ["DEV_CELERY_BROKER_URL"]
    CELERY_RESULT_BACKEND = os.environ["DEV_CELERY_RESULT_BACKEND"]
elif STATE == "local_testing":
    DB_URI_WORKER = os.environ["TEST_LOCAL_DATABASE_URI_WORKER"]
    CELERY_BROKER_URL = os.environ["TEST_LOCAL_CELERY_BROKER_URL"]
    CELERY_RESULT_BACKEND = os.environ["TEST_LOCAL_CELERY_RESULT_BACKEND"]
elif STATE == "testing":
    DB_URI_WORKER = os.environ["TEST_DATABASE_URI_WORKER"]
    CELERY_BROKER_URL = os.environ["TEST_CELERY_BROKER_URL"]
    CELERY_RESULT_BACKEND = os.environ["TEST_CELERY_RESULT_BACKEND"]
elif STATE == "production":
    DB_URI_WORKER = os.environ["PROD_DATABASE_URI_WORKER"]
    CELERY_BROKER_URL = os.environ["PROD_CELERY_BROKER_URL"]
    CELERY_RESULT_BACKEND = os.environ["PROD_CELERY_RESULT_BACKEND"]
else:
    pass

celery = Celery("tasks", broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

con = sqlalchemy.create_engine(DB_URI_WORKER)
Session = sessionmaker(bind=con)
session = Session()


### TASKS ###


@celery.task(bind=True, name="get_text")
def get_text(self, url):

    try:
        task_id = self.request.id
        url_text = extract_text_from_html(url)

        text = Text(url, str(task_id), url_text)
        session.add(text)
        session.commit()

        return ""

    except Exception as e:
        return "ERROR " + str(e)
