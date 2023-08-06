# -*- coding: utf-8 -*-
import sys

sys.path.append(sys.modules['__main__'])


from flask import Flask

from aishowapp.ext import init_ext
from aishowapp.apis import init_api
from config import configs


def app_create(env):

    app = Flask(__name__)
    app.config.from_object(configs[env])
    init_ext(app)
    init_api(app)
    # app.config["SQLALCHEMY_ECHO"] = True

    return app

