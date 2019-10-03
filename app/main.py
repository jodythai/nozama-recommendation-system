"""
This module is the main flask application.
"""

import firebase_admin
from flask import Flask

from blueprints import *


# Initialize Firebase Admin SDK.
# See https://firebase.google.com/docs/admin/setup for more information.
firebase = firebase_admin.initialize_app()

app = Flask(__name__)
app.secret_key = b'Project Imago'

# App Settings
app.config['MODEL_PATH'] = 'models/'
app.config['UPLOAD_PATH'] = 'uploads/'
app.config['PREDICT_IMAGE_WIDTH'] = 224
app.config['PREDICT_IMAGE_HEIGHT'] = 224


app.register_blueprint(home_page)
app.register_blueprint(recommend)
app.register_blueprint(signin)
app.register_blueprint(admin_home)


if __name__ == '__main__':
    app.run(debug=False)