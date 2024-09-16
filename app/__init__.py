from flask import Flask


def create_app():
    app = Flask(__name__)

    from app.home_controller import home
    app.register_blueprint(home, url_prefix='/')

    from app.changelog_controller import changelog
    app.register_blueprint(changelog, url_prefix='/changelog')
    
    return app