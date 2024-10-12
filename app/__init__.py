from flask import Flask
from flask_socketio import SocketIO

def create_app():
    app = Flask(__name__)

    from app.home_controller import home
    app.register_blueprint(home, url_prefix='/')

    from app.chat_controller import chat
    app.register_blueprint(chat, url_prefix='/chat')

    from app.spotify_controller import spotify
    app.register_blueprint(spotify, url_prefix='/spotify')

    from app.changelog_controller import changelog
    app.register_blueprint(changelog, url_prefix='/changelog')

    from app.casaos_controller import casaos
    app.register_blueprint(casaos, url_prefix='/casaos')
    
    socketio = SocketIO(app=app)

    return app, socketio