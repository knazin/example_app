import os
from celery import Celery

from dotenv import load_dotenv

load_dotenv(dotenv_path="../.env")

STATE = os.environ["CONFIG_TYPE"]

if STATE == "development":
    CELERY_BROKER_URL = os.environ["DEV_CELERY_BROKER_URL"]
    CELERY_RESULT_BACKEND = os.environ["DEV_CELERY_RESULT_BACKEND"]
elif STATE == "local_testing":
    CELERY_BROKER_URL = os.environ["TEST_LOCAL_CELERY_BROKER_URL"]
    CELERY_RESULT_BACKEND = os.environ["TEST_LOCAL_CELERY_RESULT_BACKEND"]
elif STATE == "testing":
    CELERY_BROKER_URL = os.environ["TEST_CELERY_BROKER_URL"]
    CELERY_RESULT_BACKEND = os.environ["TEST_CELERY_RESULT_BACKEND"]
elif STATE == "production":
    CELERY_BROKER_URL = os.environ["PROD_CELERY_BROKER_URL"]
    CELERY_RESULT_BACKEND = os.environ["PROD_CELERY_RESULT_BACKEND"]
else:
    pass

celery = Celery("tasks", broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)
