from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Restaurant

import json
import random
# Create your views here.

def res_view(request, restaurant_id):
    if request.method == "GET":
        restaurant = Restaurant.objects.get(id=restaurant_id)
        print(type(restaurant))
        return render(request, 'main/res_view.html', {'restaurant': restaurant})

def basic_view(request):
    if request.method=='GET':
        # Restaurants = Restaurant.objects.all()
        res_count = Restaurant.objects.count() # 음식점 전체 데이터 갯수
        random_ids = random.choices(range(res_count+1), k=5) # K개만 가져오기, LIST
        random_restaurants = Restaurant.objects.filter(id__in=random_ids)  # Queryset List
        return render(request, 'main/scoring.html', {'random_restaurants' : random_restaurants, 'random_ids':random_ids})

def put_score(request):
    if request.method=='POST':
        current_user = request.user
        data = json.loads(request.body)
        username = current_user.username

        score = data['score']        
        print(score, username)
        #@TODO Score Table 에 저장

        return JsonResponse({'msg':'Score 저장 완료'})

def main_view(request):
    if request.method=='GET':
        print('main_view 옴')
        return render(request, 'main/main.html')