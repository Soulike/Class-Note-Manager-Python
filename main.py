import os

from flask import Flask

from components import *
from database import connectDatabase
from functions import *
from routers import routers

# 读取设置文件
try:
    config = readConfigFile()
    LISTEN_PORT = config['Server']['ListenPort']
    DATABASE_NAME = config['Database']['Name']
    DATABASE_ADDRESS = config['Database']['Address']
    DATABASE_PORT = config['Database']['Port']
    DATABASE_USERNAME = config['Database']['Username']
    DATABASE_PASSWORD = config['Database']['Password']

    app = Flask(__name__, static_url_path = '')

    app.secret_key = os.urandom(24)


    @app.route('/', methods = ['GET'])
    def root():
        return app.send_static_file('index.html')


    routers.registerRouters(app)
    connectDatabase(DATABASE_ADDRESS, DATABASE_PORT, DATABASE_NAME, DATABASE_USERNAME, DATABASE_PASSWORD)

    if __name__ == '__main__':
        log('服务器运行在 {0} 端口上'.format(LISTEN_PORT))
        app.run(host = '0.0.0.0', port = LISTEN_PORT, debug = True)

except FileNotFoundError:
    log('找不到配置文件，服务器退出')
    exit(0)
