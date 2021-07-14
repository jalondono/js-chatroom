#!/bin/sh
sudo docker-compose build
sudo docker-compose up -d
sudo docker-compose run django python3 manage.py migrate
