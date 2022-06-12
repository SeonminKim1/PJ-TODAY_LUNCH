#!/bin/bash

find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete

echo "migrations/ .py, .pyc 삭제 완료"

rm -rf recommandation/restaurant.csv
echo "restaurant.csv 삭제 완료"

rm -rf static/img
echo "img 바로가기 삭제 완료"

rm -rf db.sqlite3
echo "db.sqlite3 삭제 완료"
