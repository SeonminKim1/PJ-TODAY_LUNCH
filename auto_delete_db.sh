#!/bin/bash

find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete

echo "migrations/ .py, .pyc 삭제 완료"

rm db.sqlite3
echo "db.sqlite3 삭제 완료"
