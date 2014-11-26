# Image resizer
## Installation
### Ubuntu server
```
sudo apt-get update
sudo apt-get install nginx
sudo apt-get install build-essential python-dev python-pip
sudo apt-get install libtiff5-dev libjpeg8-dev zlib1g-dev \
    libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk
```
### Virtual environment
```
sudo pip install virtualenv
sudo pip install virtualenvwrapper
export WORKON_HOME=~/.virtualenvs
mkvirtualenv resizer
workon resizer
```
### Python stuff
```
pip install -r requirements.txt
```
###Directories
Create original directory and assets directory in the same folder as app.py
## Running using nginx, upstart and uwsgi
Copy resizer.conf to /etc/init
Copy nginx_conf to /etc/nginx/sites-available/default
Make sure resizer.sh is executable
```
sudo service resizer start
sudo service nginx restart
```

## Usage
### Width and height
Url pattern url/to/file/<width>/<height>/filename.png
### Keep ratio
Use the same pattern as above but replace either width or height with "x"
