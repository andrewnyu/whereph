from flask import Flask
from flask import Blueprint, url_for
from config import Config
import os
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import pandas as pd
import geopandas as gpd
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

#load shape file
SHAPES_PATH = 'app/static/shapefile'
SHAPE_FILE = gpd.read_file(os.path.join(SHAPES_PATH, "gadm36_PHL_shp", "gadm36_PHL_3.shp"))

#Upload folder
UPLOAD_FOLDER = 'app/static/uploads'


#Database
db = SQLAlchemy()
migrate = Migrate()

#Login Manager
login = LoginManager()
login.login_view = 'auth.login'



def create_app(config_class=Config):

    #Set configuration variables
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config['UPLOAD_FOLDER'] = 'static/uploads'
    #special workaround to allow emojis in connection
    app.config['MYSQL_DATABASE_CHARSET'] = 'utf8mb4'

    #Initialize
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    #import bluepriunts
    from app.main import bp as main_bp
    from app.auth import bp as auth_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/whereph.log',
                                           maxBytes=10240, backupCount=10)
        
        #temporarily commented out since logger giving error of KeyError messageW
        
        #file_handler.setFormatter(logging.Formatter(
        #    '%(asctime)s %(levelname)s: %(messageW)s '
        #    '[in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('WherePH startup')

    return app


from app import models