import os
import django
import sys

#환경변수 세팅(뒷부분은 프로젝트명.settings로 설정한다.) 모델을 불러오는 코드 보다 위에 있어야한다
print('==추가한 Path:', os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))) # path 추가
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "today_lunch.settings")
django.setup()

from star.models import star
from restaurant.models import Restaurant
import pandas as pd

restaurant_data = Restaurant.objects.all()
star_data = star.objects.all()

df1 = pd.DataFrame(columns=['restaurant_id',
                            'restaurant_name',
                            'restaurant_address',
                            'restaurant_category_id',
                            'restaurant_image'])
df2 = pd.DataFrame(columns=['user_id',
                            'restaurant_id',
                            'star_score',
                            'star_date'])

for res in restaurant_data:
    df1 = df1.append({
        'restaurant_id': res.id,
        'restaurant_name': res.restaurant_name,
        'restaurant_address': res.restaurant_address,
        'restaurant_category_id': res.restaurant_category_id,
        'restaurant_image': res.restaurant_image,
    }, ignore_index=True)
for star in star_data:
    df2 = df2.append({
        'user_id': star.star_user_id,
        'restaurant_id': star.star_restaurant_id,
        'star_score': star.star_score,
        'star_date': star.star_date,
    }, ignore_index=True)

df1.to_csv('res_info.csv', index=False)
print('res_info.csv create success')
df2.to_csv('stars.csv', index=False)
print('stars.csv create success')