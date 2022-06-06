import pandas as pd
import numpy as np
import os

restaurants = pd.read_csv('res_info.csv')
stars = pd.read_csv('stars.csv')

# 데이터프레임을 출력했을때 더 많은 열이 보이도록 함
pd.set_option('display.max_columns', 10)
pd.set_option('display.width', 300)
# restaurant_id를 기준으로 restaurants 와 starts 를 결합함
restaurant_stars = pd.merge(restaurants, stars, on='restaurant_id')
print(restaurant_stars)

# user별로 restaurant에 부여한 star 값을 볼 수 있도록 pivot table 사용
restaurant_user = restaurant_stars.pivot_table('star_score', index='user_id', columns='restaurant_name')

# 평점을 부여안한 영화는 그냥 0이라고 부여
restaurant_user = restaurant_user.fillna(0)
print(restaurant_user)

from sklearn.metrics.pairwise import cosine_similarity

# 유저와 유저 간의 코사인 유사도를 구함
user_based_collab = cosine_similarity(restaurant_user, restaurant_user)
print(user_based_collab)

# 위는 그냥 numpy 행렬이니까, 이를 데이터프레임으로 변환
user_based_collab = pd.DataFrame(user_based_collab, index=restaurant_user.index, columns=restaurant_user.index)
print(user_based_collab)

# 1번 유저와 비슷한 유저를 내림차순으로 정렬한 후에, 상위 10개만 뽑음
print(user_based_collab[1].sort_values(ascending=False)[:10])

# 상위 유저 중 첫번째 유저를 뽑고,
user = user_based_collab[1].sort_values(ascending=False)[:10].index[1]
# 3번 유저가 좋아했던 음식점를 평점 내림차순으로 출력
result = restaurant_user.query(f"user_id == {user}").sort_values(ascending=False, by=user, axis=1)
print(result)

# 만약 해당 유저가 아직 먹어본적 없는 음식점에 대해서, 평점을 예측하고자 한다면?
# (어떤 유저와 비슷한 정도 * 그 유저가 영화에 대해 부여한 평점) 을 더해서 (유저와 비슷한 정도의 합)으로 나눠보면 됨!
# index_list 는 비슷한 유저의 id 값 리스트 / weight_list 는 비슷한 유저와의 유사도 리스트
user_index_list = user_based_collab[1].sort_values(ascending=False)[:10].index.tolist()
user_weight_list = user_based_collab[1].sort_values(ascending=False)[:10].tolist()
print(user_index_list)
print(user_weight_list)

# 1번 유저가 각음식점에 어떤 평점을 부여할지 예측
restaurant_name = '타코벨-역삼점'
weighted_sum = []
weighted_user = []
for i in range(1, 5):
    # 해당 영화를 보고 평점을 부여한 사람들의 유사도와 평점만 추가 (즉, 0이 아닌 경우에만 계산에 활용)
    if int(restaurant_user[restaurant_name][user_index_list[i]]) is not 0:
        # 평점 * 유사도 추가
        weighted_sum.append(restaurant_user[restaurant_name][user_index_list[i]] * user_weight_list[i])
        # 유사도 추가
        weighted_user.append(user_weight_list[i])

print(weighted_sum)
print(weighted_user)
# 총 평점*유사도 / 총 유사도를 토대로 평점 예측
print(sum(weighted_sum)/sum(weighted_user))
