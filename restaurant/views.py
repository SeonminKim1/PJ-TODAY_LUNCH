from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Restaurant
from star.models import star

import json
import random
from datetime import datetime

def res_view(request, restaurant_id):
    if request.method == "GET":
        restaurant = Restaurant.objects.get(id=restaurant_id)
        print(type(restaurant))
        return render(request, 'main/res_view.html', {'restaurant': restaurant})

def scoring_view(request):
    if request.method=='GET':
        # Restaurants = Restaurant.objects.all()
        res_count = Restaurant.objects.count() # 음식점 전체 데이터 갯수
        
        # 기존에 뽑았던 이력 있는지 Star Table 조회 
        random_ids = []
        while len(random_ids) != 5:
            random_id = random.randint(1, res_count)
            results = star.objects.filter(
                star_user_id = request.user.id,
                star_restaurant_id = random_id
            )
            # print(results, random_id)
            # Star table 조회했더니 경험(x)  +  이번에 뽑힌거(x)
            if (len(results)==0) and (random_id not in random_ids):
                # print('추가됨', random_id)
                random_ids.append(random_id)
        # random_ids = random.choices(range(res_count), k=5) # K개만 가져오기, LIST
        random_restaurants = Restaurant.objects.filter(id__in=random_ids)  # Queryset List
        return render(request, 'main/scoring.html', {'random_restaurants' : random_restaurants, 'random_ids':random_ids})

def put_score(request):
    if request.method=='POST':
        current_user = request.user
        data = json.loads(request.body)
        score = data['score']    
        print(score)
        
        for k, v in score.items():
            star.objects.create(
                star_avg_score = v, star_date = datetime.now().date(),
                star_restaurant = Restaurant.objects.get(id=k), star_user = current_user
            )
            # print('== 저장되는 star ', star)
        return JsonResponse({'msg':'추천 정보 기록 완료~'})

def main_view(request):
    if request.method=='GET':
        print('main_view 옴')
        return render(request, 'main/main.html')