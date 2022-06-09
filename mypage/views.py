from difflib import restore
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from datetime import datetime

from .models import Diary
from restaurant.models import Restaurant
from star.models import Star

import json

# 달력 만드는 함수
def get_calendar(year, month):
    def isLeapYear(year):
        return year % 4 == 0 and year % 100 != 0 or year % 400 == 0

    def lastDay(year, month):
        m = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        m[1] = 29 if isLeapYear(year) else 28
        return m[month - 1]

    def totalDay(year, month, day):
        total = (year - 1) * 365 + (year - 1) // 4 - (year - 1) // 100 + (year - 1) // 400
        for i in range(1, month):
            total += lastDay(year, i)
        return total + day

    def weekDay(year, month, day):
        return totalDay(year, month, day) % 7

    day_list = []
    for day in range(weekDay(year, month, 1)):
        day_list.append('  ')
    # 1일 부터 달력을 출력할 달의 마지막 날짜까지 반복하며 달력을 출력한다.
    for day in range(1, lastDay(year, month) + 1): # i가 1부터 해당 달의 마지막 날짜의 수까지 변하는 동안.
        day_list.append(day)

    for day in range(35-len(day_list)):
        day_list.append('  ')

    # days_list = []
    # for m in range(1, 6):
    #    days_list.append(day_list[0+(7*(m-1)):7*m])

    return day_list # [ [ ' ', ' ', 1, 2, 3, 4, 5], [6,7,8 ... ], [ ] ... [30, 31, ' ', ' '] ] 

# 월별 Calendar View
def mypage_view(request, year, month):
    if request.method=='GET':
        date_list = get_calendar(year, month) # 35개의 1차원 배열
        is_date_list = [False if i=='  ' else True for i in date_list ] # 35개의 1차원 배열
        # print('===request.user.id', request.user.id)
        results = Diary.objects.filter(
                diary_user_id = request.user.id,
        ).order_by('diary_date')


        diary_date_list = [datetime(year, month, day).date() if day!= '  ' else '' for day in date_list ]
        # print('===1', diary_date_list, type(diary_date_list[0]))

        # DB를 각 항 목 LIST 화        
        diary_id, diary_score, diary_restaurant_id, diary_user_id = [], [], [], []
        for diary_date in diary_date_list: # 2022-06-01 ~ 2022-06-30
            ok = False
            # DB에 있는지 체크
            for re in results:
                # print('===sibal==', diary_date, type(diary_date), re.diary_date, type(re.diary_date))
                if re.diary_date ==  diary_date:
                    diary_id.append(re.id)
                    diary_score.append(re.diary_score)                    
                    diary_restaurant_id.append(re.diary_restaurant_id)                    
                    diary_user_id.append(re.diary_user_id)                    
                    ok = True
                    break
                else:
                    continue
            if ok == False: # 만약 DB에 없는 거면.
                diary_id.append(None)
                diary_score.append(None)                    
                diary_restaurant_id.append(None)                    
                diary_user_id.append(None) 
        is_diary_list = [False if ds==None else True for ds in diary_score ]
        days = ['월','화','수','목','금','토','일']
        diary_weekday_list = list(map(lambda x: days[x.weekday()] if x!='' else '', diary_date_list))
        diary_date_list = list(map(lambda x : datetime.strftime(x, '%Y-%m-%d') if x !='' else '', diary_date_list)) # datetime.date to string
        print('================')
        print('date_list :', date_list, len(date_list)) # ' ',' ', '1', '2' ... '31'
        print('is_date_list :', is_date_list, len(is_date_list)) # True, False 
        print('diary_id :', diary_id, len(diary_id)) # [1, 2, 3, 4]
        print('diary_weekday_list:', diary_weekday_list, len(diary_weekday_list)) # ['수','목','금'...]
        print('diary_date_list :', diary_date_list, len(diary_date_list)) # ['2022-06-02', '2022-06-03'... '2022-06-30']
        print('diary_score :', diary_score, len(diary_score)) # [3, 4, 5, 2, 1, ...]
        print('is_diary_list :', is_diary_list, len(is_diary_list)) # by score [True, False, False ...]
        print('diary_restaurant_id :', diary_restaurant_id, len(diary_restaurant_id)) # [37, 25, 131, 86 ...]
        print('diary_user_id :', diary_user_id, len(diary_user_id)) # [1,1,1,1,2,2,2]
        print('=================')

        result_date_list= []
        for day, is_day, id, date, weekday, is_diary, score, restaurant_id \
            in zip(date_list, is_date_list, diary_id, diary_date_list, diary_weekday_list, is_diary_list, diary_score, diary_restaurant_id):
            result_date_list.append(
                {
                    'day': day,
                    'is_date':is_day,
                    'id': id,
                    'date': date, # 2022-06-17,
                    'weekday':weekday, # '월'
                    'is_diary':is_diary,
                    'restaurant_score':score,
                    'restaurant_name':restaurant_id,
                }
            )
                
        
        print('====최종 dict===', result_date_list[3])
        print('====최종 dict===', result_date_list[7])
        
        # 한 주씩 끊어서.
        final_results = []
        for m in range(1, 6):
            final_results.append(result_date_list[0+(7*(m-1)):7*m])

        # 가게 이름 list
        resturant_name_list = list(map(lambda x: x.restaurant_name, Restaurant.objects.filter().only('restaurant_name')))
        # print('=====', resturant_name_list, len(resturant_name_list))
        return render(request, 'mypage/mypage.html', {'calendar':final_results, 'year':year, 'month':month, 'resturant_name_list':resturant_name_list})

def create_diary(request):
    if request.method=='POST':
        data = json.loads(request.body)
        date = data['date_val'] # data['weekday_val'] : 요일
        restaurant_name = data['search_val'] 
        score = int(data['score_val'])
        user_id = request.user.id

        ### Diary Table Create
        Diary.objects.create(
            diary_user_id = user_id,
            diary_date = date,
            diary_restaurant = Restaurant.objects.get(restaurant_name = restaurant_name),
            diary_score = score
        )
        
        ### Restaurant Table 값 Update
        # 1) Restaurant_name으로 조회
        # 2) Restaurant_Count를 count+1로 Restaurant_Avg_score 재계산
        diary_resturant = Restaurant.objects.get(restaurant_name = restaurant_name)
        update_count = diary_resturant.restaurant_count + 1
        update_avg_score = ((diary_resturant.restaurant_avg_score * diary_resturant.restaurant_count) + score) / update_count
        Restaurant.objects.filter(restaurant_name = restaurant_name)\
            .update(
                restaurant_count = update_count,
                restaurant_avg_score = update_avg_score
            )

        ### Star Table 값 Create & Update 
        # 0) Star Table은 User_id가 Restaurant_id를 평가한 정보 (Max Record 갯수 User_id * Restaurant_id)
        # 1) user id와 restaurant_id로 해당 정보에 접근
        # 2) Star Table이 없으면 Create 
        # 3) Star Table이 있으면 Update 
        diary_restaurant_id = diary_resturant.id
        try:
            diary_star = Star.objects.get(star_restaurant_id = diary_restaurant_id, star_user_id = user_id)
        except:
            diary_star = None
        if diary_star == None:
            print('=== 해당 유저는 해당 음식점을 평가하는 것이 처음 입니다. ')
            Star.objects.create(
                star_date = datetime.strftime(datetime.today(), '%Y-%m-%d'), # last update date
                star_avg_score = score,
                star_restaurant_id = diary_restaurant_id, 
                star_user_id = user_id
            )
        else:
            update_count = diary_star.star_count + 1
            update_avg_score = ((diary_star.star_avg_score * diary_star.star_count) + score) / update_count
        
            Star.objects.filter(star_restaurant_id = diary_restaurant_id, star_user_id = user_id)\
                .update(
                    star_date = datetime.strftime(datetime.today(), '%Y-%m-%d'), # last update date
                    star_avg_score = update_avg_score,
                    star_restaurant_id = diary_restaurant_id, 
                    star_user_id = user_id,
                    star_count = update_count
                )

        return JsonResponse({'msg':'Diary 등록 완료!'})
    # 


def update_diary(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        date = data['date_val']  # data['weekday_val'] : 요일
        restaurant_name = data['search_val']
        score = int(data['score_val'])
        user_id = request.user.id

        ### Diary Table Create
        Diary.objects.create(
            diary_user_id=user_id,
            diary_date=date,
            diary_restaurant=Restaurant.objects.get(restaurant_name=restaurant_name),
            diary_score=score
        )

        ### Restaurant Table 값 Update
        # 1) Restaurant_name으로 조회
        # 2) Restaurant_Count를 count+1로 Restaurant_Avg_score 재계산
        diary_resturant = Restaurant.objects.get(restaurant_name=restaurant_name)
        update_count = diary_resturant.restaurant_count + 1
        update_avg_score = ((
                                        diary_resturant.restaurant_avg_score * diary_resturant.restaurant_count) + score) / update_count
        Restaurant.objects.filter(restaurant_name=restaurant_name) \
            .update(
            restaurant_count=update_count,
            restaurant_avg_score=update_avg_score
        )

        ### Star Table 값 Create & Update
        # 0) Star Table은 User_id가 Restaurant_id를 평가한 정보 (Max Record 갯수 User_id * Restaurant_id)
        # 1) user id와 restaurant_id로 해당 정보에 접근
        # 2) Star Table이 없으면 Create
        # 3) Star Table이 있으면 Update
        diary_restaurant_id = diary_resturant.id
        try:
            diary_star = Star.objects.get(star_restaurant_id=diary_restaurant_id, star_user_id=user_id)
        except:
            diary_star = None
        if diary_star == None:
            print('=== 해당 유저는 해당 음식점을 평가하는 것이 처음 입니다. ')
            Star.objects.create(
                star_date=datetime.strftime(datetime.today(), '%Y-%m-%d'),  # last update date
                star_avg_score=score,
                star_restaurant_id=diary_restaurant_id,
                star_user_id=user_id
            )
        else:
            update_count = diary_star.star_count + 1
            update_avg_score = ((diary_star.star_avg_score * diary_star.star_count) + score) / update_count

            Star.objects.filter(star_restaurant_id=diary_restaurant_id, star_user_id=user_id) \
                .update(
                star_date=datetime.strftime(datetime.today(), '%Y-%m-%d'),  # last update date
                star_avg_score=update_avg_score,
                star_restaurant_id=diary_restaurant_id,
                star_user_id=user_id,
                star_count=update_count
            )

        return JsonResponse({'msg': 'Diary 등록 완료!'})
    #