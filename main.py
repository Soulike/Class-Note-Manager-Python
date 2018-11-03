from components import *
from functions import *
from flask import Flask
from database import connectDatabase
from routers import routers

# 读取设置文件
try:
    config = readConfigFile()
except FileNotFoundError:
    log('找不到配置文件，服务器退出')
    exit(0)

LISTEN_PORT = config['Server']['ListenPort']
DATABASE_NAME = config['Database']['Name']
DATABASE_ADDRESS = config['Database']['Address']
DATABASE_PORT = config['Database']['Port']
DATABASE_USERNAME = config['Database']['Username']
DATABASE_PASSWORD = config['Database']['Password']

app = Flask(__name__, static_url_path = '')


@app.route('/', methods = ['GET'])
def root():
    return app.send_static_file('index.html')


routers.registerRouters(app)
connectDatabase(DATABASE_ADDRESS, DATABASE_PORT, DATABASE_NAME, DATABASE_USERNAME, DATABASE_PASSWORD)

if __name__ == '__main__':
    log('服务器运行在 {0} 端口上'.format(LISTEN_PORT))
    app.run(host = '0.0.0.0', port = LISTEN_PORT, debug = True)
