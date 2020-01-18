#!/usr/bin/env bash

# Consider running these two commands separately
# Do a reboot before continuing.
sudo apt update
sudo apt upgrade -y

sudo apt install zsh
# What is this for?
#sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"

# Install some OS dependencies:
sudo apt-get install -y -q build-essential git unzip zip nload tree
sudo apt-get install -y -q python3-pip python3-dev python3-venv
sudo apt-get install -y -q nginx
# for gzip support in uwsgi
sudo apt-get install --no-install-recommends -y -q libpcre3-dev libz-dev

# Stop the hackers - blacklists people that fail to login repeatedly via ssh
sudo apt install fail2ban -y

# Allow ports we needed (is this necessary for AWS?  I didn't bother)
#ufw allow 22
#ufw allow 80
#ufw allow 443
#ufw enable

# Basic git setup
# Remember my credentials for a month before I for them
git config --global credential.helper cache
git config --global credential.helper 'cache --timeout=720000'

# Be sure to put your info here:
git config --global user.email "ca.scribner@gmail.com"
git config --global user.name "Andrew Scribner"

# Web app file structure
sudo mkdir /apps
sudo chmod 777 /apps
sudo mkdir /apps/logs
sudo mkdir /apps/logs/pypi
sudo mkdir /apps/logs/pypi/app_log
cd /apps

# Create a virtual env for the app.
cd /apps
python3 -m venv venv
source /apps/venv/bin/activate
pip install --upgrade pip setuptools
pip install --upgrade httpie glances
pip install --upgrade uwsgi

# To reconfigure our venv every time we add in, also add this to your .zshrc (or bash equiv)
# source/apps/venv/bin/activate
# This way we don't have to reactivate every login

# clone the repo:
cd /apps
git clone https://github.com/ca-scribner/PyPI-in-Flask app_repo

# Setup the web app:
cd cd /apps/app_repo/
pip install -r requirements.txt

# Need a step here where I create our fake db.  In real applications we'd query an actual DB, not this local file,
# so this wouldn't be necessary


# Copy and enable the daemon
sudo cp /apps/app_repo/server/pypi.service /etc/systemd/system/pypi.service

# Start this as a service
sudo systemctl start pypi
# Look at it running
sudo systemctl status pypi
# Enable it as a service when system starts (so if we reboot, it will be up for us again automatically)
sudo systemctl enable pypi

# Setup the public facing server (NGINX)
sudo apt install nginx

# CAREFUL HERE. If you are using default, maybe skip this
sudo rm /etc/nginx/sites-enabled/default

sudo cp /apps/app_repo/server/pypi.nginx /etc/nginx/sites-enabled/pypi.nginx
sudo update-rc.d nginx enable
sudo service nginx restart


# Optionally add SSL support via Let's Encrypt:
# https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-18-04

add-apt-repository ppa:certbot/certbot
apt install python-certbot-nginx
certbot --nginx -d fakepypi.talkpython.com
