# -*- coding: utf-8 -*-
import os
# import logging

from flask_script import Manager, Shell
from flask_migrate import MigrateCommand

from aishowapp import app_create
from aishowapp.ext import db
# from aishowapp.models import resource_model

app = app_create(os.getenv('FLASK_CONFIG') or 'default')

manager = Manager(app)

@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db)


# manager.add_command("shell", Shell(make_context=make_shell_context))
# manager.add_command('db', MigrateCommand)
#
if __name__ == '__main__':

    app.debug = True
    # handler = logging.FileHandler('flask.log', encoding='UTF-8')
    # handler.setLevel(logging.DEBUG)
    # logging_format = logging.Formatter(
    #     '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
    # handler.setFormatter(logging_format)
    # app.logger.addHandler(handler)
    # manager.run()

    #线上部署ip+端口
    # app.run(host='127.0.0.1', port=8001)
    # app.run(host='0.0.0.0', port=8001)
    #笔记本ip+端口
    # app.run(host='192.168.1.121', port=8080)
    # app.run(host='127.0.0.1', port=8080)
    #台式机ip
    app.run(host='192.168.0.55', port=8080)

