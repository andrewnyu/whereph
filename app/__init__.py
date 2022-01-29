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

#load shape file
SHAPES_PATH = 'app/static/shapefile'
#PKL_SHAPE_FILE = os.path.join(SHAPES_PATH, 'ph-shape.pkl')
#SHAPE_FILE = pd.read_pickle(PKL_SHAPE_FILE)
SHAPE_FILE = gpd.read_file(os.path.join(SHAPES_PATH, "gadm36_PHL_shp", "gadm36_PHL_3.shp"))


UPLOAD_FOLDER = 'app/static/uploads'



def create_app(config_class=Config):


    app = Flask(__name__)
    app.config.from_object(config_class)

    app.config['UPLOAD_FOLDER'] = 'static/uploads'

    #special workaround to allow emojis in connection
    app.config['MYSQL_DATABASE_CHARSET'] = 'utf8mb4'


    db = SQLAlchemy(app)
    migrate = Migrate(app, db)

    #import bluepriunts
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    if not app.debug and not app.testing:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'],
                        app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject='WherePH Failure',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

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

