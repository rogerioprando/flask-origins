import os
import logging

SECRET_KEY = 'Rest&gaze=Music-tin-falcon!bunk'
SQLALCHEMY_DATABASE_URI = 'postgresql://origins:origins@localhost:5432/dev_origins'

WTF_CSRF_ENABLED = True
WTF_CSRF_SECRET_KEY = 'career5Why+Glossy=When7Stereo4accept'

TEMPLATES_AUTO_RELOAD = True

LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOGGING_LOCATION = 'origins.log'
LOGGING_LEVEL = logging.DEBUG

DEBUG = True
SQLALCHEMY_ECHO = True
USE_RELOADER = True

RUN_HOST = '0.0.0.0'
RUN_PORT = int(os.environ.get('PORT', 8000))

# grab the folder of the top-level directory of this project
BASEDIR = os.path.abspath(os.path.dirname(__file__))
APP_DIR = os.path.abspath(os.curdir)

UPLOADS_DEFAULT_DEST = APP_DIR + '/brain/static/uploads/'
UPLOADS_DEFAULT_URL = 'http://{}:{}/{}'.format(RUN_HOST, RUN_PORT, 'static/uploads/')

UPLOADED_IMAGES_DEST = APP_DIR + '/brain/static/uploads/images/'
UPLOADED_IMAGES_URL = 'http://{}:{}/{}'.format(RUN_HOST, RUN_PORT, 'static/uploads/images/')
