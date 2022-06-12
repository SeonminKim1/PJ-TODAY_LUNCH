#!/bin/bash

python3 manage.py makemigrations
python3 manage.py migrate
echo "==== makemigrations, migrate 완료"

# sudo python3 auto_change_img-path.py

echo "==== Change img-path 완료"

python3 recommandation/db_uploader.py
echo "==== Restaurant DB Upload 완료"

python3 manage.py runserver 0:8000
