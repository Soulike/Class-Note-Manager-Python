from .NoteManagement import NoteManagement
from .Login import Login


def registerRouters(app):
    app.register_blueprint(NoteManagement, url_prefix = '/server')
    app.register_blueprint(Login, url_prefix = '/server')
