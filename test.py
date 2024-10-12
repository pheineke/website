from app import create_app

app, socketio = create_app()
app.config['TEMPLATES_AUTO_RELOAD'] = True

if __name__ == '__main__':
    app.run()