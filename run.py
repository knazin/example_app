import os 
import time

import sqlalchemy
from app import update_app, app
from app.api.models import db

config_type = os.environ['CONFIG_TYPE']
application = update_app(app, db, config_type)

if __name__ == "__main__":

    with application.app_context():
        if config_type != 'production':
            db.session.remove()
            db.reflect()
            db.drop_all()
        db.create_all()

    application.run(host='0.0.0.0', port=5000, debug=True)