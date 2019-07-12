import os 
import time

import sqlalchemy
from app import update_app, app

config_type = os.environ['CONFIG_TYPE']
application = update_app(app, config_type)

if __name__ == "__main__":
    application.run(host='0.0.0.0', port=5000, debug=True)