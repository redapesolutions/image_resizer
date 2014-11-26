#!/bin/bash

NAME="resizer"                                  # Name of the application
FLASKDIR=/home/azureuser           # Django project directory
LOG_FILE=/home/azureuser/logs/uwsgi.log
NUM_WORKERS=3                                     # how many worker processes should Gunicorn spawn
WSGI_MODULE=app.py                 # WSGI module name
# Vurtual env dir
PORT=3031
VIRTUAL_ENV_DIR=/home/azureuser/.virtualenvs/resizer
echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $FLASKDIR
source ${VIRTUAL_ENV_DIR}/bin/activate
export PYTHONPATH=$FLASKDIR:$PYTHONPATH

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec ${VIRTUAL_ENV_DIR}/bin/uwsgi --socket 127.0.0.1:${PORT} --wsgi-file ${FLASKDIR}/app.py --callable app --processes ${NUM_WORKERS} --threads 2 --stats 127.0.0.1:9191 --logto=$LOG_FILE
