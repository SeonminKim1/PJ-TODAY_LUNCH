#!/bin/bash

python3 manage.py makemigrations
python3 manage.py migrate
echo "==== makemigrations, migrate 완료"

# sudo python3 auto_change_img-path.py

# echo "==== Change img-path 완료"

sudo cp /mnt/luckyseven-s3/restaurant.csv recommandation/restaurant.csv
sudo chmod 664 recommandation/restaurant.csv

echo "==== restauratnt.csv 파일 생성 완료"

ln -s /mnt/luckyseven-s3/img/ static/
echo "==== img mnt 바로가기 생성 완료"

python3 recommandation/db_uploader.py
echo "==== Restaurant DB Upload 완료"

python3 manage.py runserver 0:8000
