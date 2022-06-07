import os
import django
import sys

#환경변수 세팅(뒷부분은 프로젝트명.settings로 설정한다.) 모델을 불러오는 코드 보다 위에 있어야한다

print('==추가한 Path:', os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))) # path 추가
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "today_lunch.settings")
django.setup()

from restaurant.models import Restaurant
from star.models import Star
import pandas as pd


def initailize():
    restaurant_data = Restaurant.objects.all()
    star_data = Star.objects.all()

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

    return df1, df2


def recommandation(login_user_id):
    # 현재 DB에 맞게 동기화
    restaurants, stars = initailize()

    # 데이터프레임을 출력했을때 더 많은 열이 보이도록 함
    pd.set_option('display.max_columns', 10)
    pd.set_option('display.width', 300)
    # restaurant_id를 기준으로 restaurants 와 starts 를 결합함
    restaurant_stars = pd.merge(restaurants, stars, on='restaurant_id')
    # print(restaurant_stars)

    # user별로 restaurant에 부여한 star 값을 볼 수 있도록 pivot table 사용
    restaurant_user = restaurant_stars.pivot_table('star_score', index='user_id', columns='restaurant_name')

    # 평점을 부여안한 영화는 그냥 0이라고 부여
    restaurant_user = restaurant_user.fillna(0)
    # print(restaurant_user)

    from sklearn.metrics.pairwise import cosine_similarity

    # 유저와 유저 간의 코사인 유사도를 구함
    user_based_collab = cosine_similarity(restaurant_user, restaurant_user)
    # print(user_based_collab)

    # 위는 그냥 numpy 행렬이니까, 이를 데이터프레임으로 변환
    user_based_collab = pd.DataFrame(user_based_collab, index=restaurant_user.index, columns=restaurant_user.index)
    # print(user_based_collab)

    # 1번 유저와 비슷한 유저를 내림차순으로 정렬한 후에, 상위 10개만 뽑음
    print(user_based_collab[login_user_id].sort_values(ascending=False)[:10])

    # 상위 유저 중 첫번째 유저를 뽑고,
    user = user_based_collab[login_user_id].sort_values(ascending=False)[:10].index[1]

    # 해당 유저가 좋아했던 음식점를 평점 내림차순으로 출력
    result = restaurant_user.query(f"user_id == {user}").sort_values(ascending=False, by=user, axis=1)
    # print(result)

    result_list = []
    for re in result:
        result_list.append(re)

    # print(result_list)
    return result_list
