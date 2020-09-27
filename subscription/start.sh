#!/bin/bash

sleep 10
python3 subscription/manage.py migrate
python3 subscription/manage.py runserver 0.0.0.0:8080