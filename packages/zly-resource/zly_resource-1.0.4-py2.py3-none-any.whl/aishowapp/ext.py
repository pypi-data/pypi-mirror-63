# -*- coding: utf-8 -*-
from flask_caching import Cache
from flask_moment import Moment
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate

db=SQLAlchemy()
migrate=Migrate()
moment = Moment()
session=Session()
bootstarp = Bootstrap()
cache=Cache(config={'CACHE_TYPE':'simple'})


def init_ext(app):
    CORS(app, supports_credentials=True)
    db.init_app(app=app)
    session.init_app(app)
    moment.init_app(app)
    migrate.init_app(app, db)
    bootstarp.init_app(app)
    cache.init_app(app)