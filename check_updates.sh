#!/bin/bash

# Gehe in das Verzeichnis deines Git-Repos
cd /app/your_git_repo || exit

# Pull die neuesten Änderungen
git pull

# Starte den Flask-Server neu
touch your_flask_app.py  # Dies löst einen Reload in Flask aus, wenn du den Debug-Modus verwendest
