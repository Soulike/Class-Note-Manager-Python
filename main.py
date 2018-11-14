import atexit
import os

from flask import Flask

from components import *
from database import connectDatabase, disconnectDatabase
from functions import log
from routers import routers

try:
    try:
        # 读取设置文件
        config = readConfigFile()
    except FileNotFoundError as e:
        log('找不到配置文件，错误信息：')
        log(e)
    except IOError as e:
        log('配置文件读取失败，错误信息：')
        log(e)
    else:
        LISTEN_PORT = config['Server']['ListenPort']
        DATABASE_NAME = config['Database']['Name']
        DATABASE_ADDRESS = config['Database']['Address']
        DATABASE_PORT = config['Database']['Port']
        DATABASE_USERNAME = config['Database']['Username']
        DATABASE_PASSWORD = config['Database']['Password']
        NOTE_FILE_POSITION = config['File']['NoteFilePosition']

        # 连接数据库。如果连接失败直接退出程序
        try:
            connectDatabase(DATABASE_ADDRESS, DATABASE_PORT, DATABASE_NAME, DATABASE_USERNAME,
                            DATABASE_PASSWORD)
        except IOError as e:
            log('数据库连接失败，错误信息：')
            log(e)
        else:
            try:
                # 创建存放笔记文件用的文件夹
                os.makedirs(NOTE_FILE_POSITION, 0o777, True)
            except IOError as e:
                log('笔记存储文件夹不存在且创建失败，错误信息：')
                log(e)
            else:
                # Flask 设置
                app = Flask(__name__, static_folder = 'static/build')
                app.secret_key = os.urandom(24)

                # 注册各个路由
                routers.registerRouters(app)

                # 在应用程序退出之前关闭数据库连接
                atexit.register(disconnectDatabase)

                if __name__ == '__main__':
                    log('服务器运行在 {0} 端口上'.format(LISTEN_PORT))
                    app.run(host = '0.0.0.0', port = LISTEN_PORT, debug = False)

except Exception as e:
    log('未能捕获的错误，错误信息：')
    log(e)
