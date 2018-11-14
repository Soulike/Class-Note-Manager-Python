from .Login import Login
from .NoteManagement import NoteManagement
from .ReactApp import ReactApp


# 注册所有子路由
def registerRouters(app):
    app.register_blueprint(ReactApp)
    app.register_blueprint(NoteManagement, url_prefix = '/server')
    app.register_blueprint(Login, url_prefix = '/server')
