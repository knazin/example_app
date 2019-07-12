import os, sys, inspect

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import pytest
import psycopg2
from run import application, db
from app.api.models import Text, Image

from app.api.worker import celery

from dotenv import load_dotenv
load_dotenv(dotenv_path="../app/.env")

@pytest.fixture(scope="module")
def test_client():
    # Flask provides a way to test your application by exposing 
    # the Werkzeug test Client and handling the context locals for you.
    testing_client = application.test_client()

    # Establish an application context before running the tests.
    ctx = application.app_context()
    ctx.push()

    yield testing_client  # this is where the testing happens!

    ctx.pop()


@pytest.fixture(scope="module") # module # session 
def database():
    db.session.remove()
    db.reflect()
    db.drop_all()
    db.create_all()

    yield db  # this is where the testing happens!

    db.drop_all()


@pytest.fixture(scope="module")
def f_celery():
    yield celery


@pytest.fixture(scope="module")
def f_gettext():
    yield gettext
    

@pytest.fixture(scope="module")
def text():
    yield Text


@pytest.fixture(scope="module")
def image():
    yield Image
