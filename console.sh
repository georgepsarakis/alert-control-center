#!/bin/bash

export DATABASE_PASSWORD=alert_manager
export SECRET_KEY='something-secret!'

./src/manage.py shell
