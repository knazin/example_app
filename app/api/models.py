from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Task(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String)
    task_id = db.Column(db.String)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


class Text(Task):

    text = db.Column(db.String)

    def __init__(self, url, task_id, text):
        self.url = url
        self.task_id = task_id
        self.text = text


class Image(Task):

    name = db.Column(db.String, unique=True)
    source_url = db.Column(db.String, unique=True)
    data = db.Column(db.LargeBinary)

    def __init__(self, url, task_id, name, source_url, data):
        self.url = url
        self.task_id = task_id
        self.name = name
        self.source_url = source_url
        self.data = data