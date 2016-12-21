# 创建依赖的工厂方法
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_cache import Cache
from flask_login import LoginManager

import logging

from .config import config

bootstrap = Bootstrap()
mail = Mail()
db = SQLAlchemy()
# cache = Cache()
loginManager = LoginManager()

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='myapp.log',
                filemode='w')

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    # config[config_name].init_app(app)
    bootstrap.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    # cache.init_app(app)
    loginManager.init_app(app)
    return app



