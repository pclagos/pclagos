#!/bin/bash
# build_files.sh
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate --run-syncdb
