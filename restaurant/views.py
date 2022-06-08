from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Restaurant
from star.models import Star
from users.models import UserModel
from recommandation.recommand import recommandation

import json
import random
from datetime import datetime, timedelta



def res_view(request, restaurant_id):
    if request.method == "GET":
        restaurant = Restaurant.objects.get(id=restaurant_id)
        print(type(restaurant))
        return render(request, 'main/res_view.html', {'restaurant': restaurant})


def scoring_view(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            # Restaurants = Restaurant.objects.all()
            res_count = Restaurant.objects.count()  # 음식점 전체 데이터 갯수

            # 기존에 뽑았던 이력 있는지 Star Table 조회
            random_ids = []
            while len(random_ids) != 5:
                random_id = random.randint(1, res_count)
                results = Star.objects.filter(
                    star_user_id=request.user.id,
                    star_restaurant_id=random_id
                )
                # print(results, random_id)
                # Star table 조회했더니 경험(x)  +  이번에 뽑힌거(x)
                if (len(results) == 0) and (random_id not in random_ids):
                    # print('추가됨', random_id)
                    random_ids.append(random_id)
            # random_ids = random.choices(range(res_count), k=5) # K개만 가져오기, LIST
            random_restaurants = Restaurant.objects.filter(id__in=random_ids)  # Queryset List
            return render(request, 'main/scoring.html',
                          {'random_restaurants': random_restaurants, 'random_ids': random_ids})
        else:
            return redirect('login')

def put_score(request):
    if request.method == 'POST':
        current_user = request.user
        data = json.loads(request.body)
        score = data['score']
        print(score)

        for k, v in score.items():
            Star.objects.create(
                star_avg_score=v, star_date=datetime.now().date(),
                star_restaurant=Restaurant.objects.get(id=k), star_user=current_user
            )
            # print('== 저장되는 star ', star)

            # 레스토랑 평가 횟수, 평균 점수 update
            res = Restaurant.objects.get(id=k)
            count = res.restaurant_count
            if count == 0:
                Restaurant.objects.filter(id=k).update(restaurant_count=1)
                Restaurant.objects.filter(id=k).update(restaurant_avg_score=v)
            else:
                avg_score = (count * res.restaurant_avg_score) + v / count + 1
                Restaurant.objects.filter(id=k).update(restaurant_count=count + 1)
                Restaurant.objects.filter(id=k).update(restaurant_avg_score=avg_score)


        return JsonResponse({'msg':'추천 정보 기록 완료~'})

def main_view(request, category):
    if request.method == 'GET':
        # 현재 로그인 유저 정보 가져오기
        current_user = request.user
        user = UserModel.objects.get(id=current_user.id)

        # 사용자 기반 추천 시스템 필터링 거쳐 가장 비슷한 유저가 가본 음식점 중 평점 높은 순으로 리스트 가져옴
        reco, similar_user = recommandation(current_user.id)

        # 나와 가장 비슷한 사용자의 정보
        similar = UserModel.objects.get(id=similar_user)

        # 내가 가본 음식점들 골라 내기
        my_star = Star.objects.filter(star_user=current_user.id)
        visited_restaurant = []
        for star in my_star:
            visited_restaurant.append(star.star_restaurant.restaurant_name)

        # 추천리스트에서 내가 가본 음식점들 빼고 TOP 5개만 저장
        reco_list = list(set(reco) - set(visited_restaurant))[0:5]
        print(reco_list)

        # 추천 순위 TOP5 레스토랑의 이름으로 DB에서 검색해서 해당 object 받아와 리스트에 저장
        recos = []
        for re in reco_list:
            recos.append(Restaurant.objects.get(restaurant_name=re))

        # '오늘의 추천' - 어제 가장 높은 평점을 기록한 음식점 중 하나
        try:
            yesterday = datetime.now().date() - timedelta(days=1)
            yesterday_top = Star.objects.filter(star_date=yesterday)

            # 어제의 최고 점수, 최고점수 받은 가게 추출
            top_score = 0
            today_reco = []
            for top in yesterday_top:
                if top_score < top.star_avg_score:
                    top_score = top.star_avg_score

            for top in yesterday_top:
                if top_score == top.star_avg_score:
                    today_reco.append(top.star_restaurant.restaurant_name)

            # 추출한 가게들 중 하나만 랜덤으로 선택 해서 출력
            choice = random.choice(today_reco)
            result = 'success'
            today_res = Restaurant.objects.get(restaurant_name=choice)
        except:
            result = 'fail'
            today_res = '어제 평점이 매겨진 음식점이 없습니다.'

        # # 모두, 한식, 중식, 일식, 양식 TOP 랭킹 출력
        # if category == 1:
        #     restaurants = Restaurant.objects.all()
        #     for res in restaurants:
        #         count = Star.objects.filter(star_restaurant=res).count()
        #         star_res = Star.objects.filter(star_restaurant=res)



        return render(request, 'main/main.html', {'recos': recos,
                                                  'user': user,
                                                  'similar': similar,
                                                  'result': result,
                                                  'today_res': today_res})
