import os

from flask import Blueprint, send_from_directory

ReactApp = Blueprint('ReactApp', __name__)


@ReactApp.route('/', defaults = {'path': ''})
@ReactApp.route('/<path:path>')
def reactApp(path):
    if path != "" and os.path.exists(os.path.join('static', 'build', path)):
        return send_from_directory(os.path.join('static', 'build'), path)
    else:
        return send_from_directory(os.path.join('static', 'build'), 'index.html')
