#!/bin/bash

export DATABASE_PASSWORD=alert_manager
export SECRET_KEY='something-secret!'

exec ./src/manage.py runserver
