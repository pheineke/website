#!/bin/bash
cd /home/pi/website
git fetch origin main

LOCAL=$(git rev-parse @)
REMOTE=$(git rev-parse @{u})

if [ $LOCAL != $REMOTE ]; then
    echo "## $(date '+%Y-%m-%d %H:%M:%S') - Updates found" >> update.md
    # Get the list of new commits
    git log --oneline --pretty=format:"- %h %s" $LOCAL..$REMOTE >> update.md
    echo "" >> update.log  # Add a new line after the commit list
    # Pull the updates
    git pull origin main >> update.md 2>&1
    # Restart Gunicorn service
    sudo systemctl restart flaskapp
else
    echo "## $(date '+%Y-%m-%d %H:%M:%S') - No updates found" >> update.md
fi