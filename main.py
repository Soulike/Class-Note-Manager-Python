import os
import atexit
from flask import Flask

from components import *
from database import connectDatabase, closeDatabase
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
    NOTE_FILE_POSITION = config['File']['NoteFilePosition']

    os.makedirs(NOTE_FILE_POSITION, 0o777, True)

    app = Flask(__name__, static_url_path = '')

    app.secret_key = os.urandom(24)


    @app.route('/', methods = ['GET'])
    def root():
        return app.send_static_file('index.html')


    routers.registerRouters(app)
    connectDatabase(DATABASE_ADDRESS, DATABASE_PORT, DATABASE_NAME, DATABASE_USERNAME, DATABASE_PASSWORD)

    atexit.register(closeDatabase)  # 在应用程序退出之前关闭数据库连接

    if __name__ == '__main__':
        log('服务器运行在 {0} 端口上'.format(LISTEN_PORT))
        app.run(host = '0.0.0.0', port = LISTEN_PORT, debug = False)

except FileNotFoundError:
    log('找不到配置文件，服务器退出')
    exit(0)
