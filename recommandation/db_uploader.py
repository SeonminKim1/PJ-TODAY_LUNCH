#임포트
import os
import sys
import csv
import django

#환경변수 세팅(뒷부분은 프로젝트명.settings로 설정한다.) 모델을 불러오는 것보다 무조건 위에 있어야한다.
print('==추가한 Path:', os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))) # path 추가
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "today_lunch.settings")
django.setup()

# model import
from restaurant.models import *

print('==현재 Path:', os.getcwd())
#읽어들일 csv 디렉토리를 각 변수에 담는다.
RESTAURANT = 'recommandation/restaurant.csv'

#함수 정의하기 (row부분엔 해당 table의 row명을 적어준다.)
def insert_Restaurant():
    Categories.objects.create(restaurant_category='한식')
    Categories.objects.create(restaurant_category='중식')
    Categories.objects.create(restaurant_category='일식')
    Categories.objects.create(restaurant_category='양식')
    with open(RESTAURANT, encoding='utf-8') as csv_file:
        data_reader = csv.reader(csv_file)
        next(data_reader, None)
        for row in data_reader:
            if row[0]:
                name = row[0]
                address = row[1]
                image = row[2]
                category = row[3]
                # print(name, address, image, category)
                Restaurant.objects.create(restaurant_name=name,
                                          restaurant_address=address,
                                          restaurant_image=image,
                                          restaurant_category_id=category)
    print('MENU DATA UPLOADED SUCCESSFULY!')
#print 부분은 터미널에서 파일을 실행했을때 데이터 입력이 잘 되었는지 확인하는 용도로써 필수요소는 아니다.
# 함수 실행
insert_Restaurant()