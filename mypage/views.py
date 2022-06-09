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
    for day in range(1, lastDay(year, month) + 1):  # i가 1부터 해당 달의 마지막 날짜의 수까지 변하는 동안.
        day_list.append(day)

    for day in range(35 - len(day_list)):
        day_list.append('  ')

    # days_list = []
    # for m in range(1, 6):
    #    days_list.append(day_list[0+(7*(m-1)):7*m])

    return day_list  # [ [ ' ', ' ', 1, 2, 3, 4, 5], [6,7,8 ... ], [ ] ... [30, 31, ' ', ' '] ]


# 월별 Calendar View
def mypage_view(request, year, month):
    if request.method == 'GET':
        date_list = get_calendar(year, month)  # 35개의 1차원 배열
        is_date_list = [False if i == '  ' else True for i in date_list]  # 35개의 1차원 배열
        # print('===request.user.id', request.user.id)
        results = Diary.objects.filter(
            diary_user_id=request.user.id,
        ).order_by('diary_date')

        diary_date_list = [datetime(year, month, day).date() if day != '  ' else '' for day in date_list]
        # print('===1', diary_date_list, type(diary_date_list[0]))

        # DB를 각 항 목 LIST 화        
        diary_id, diary_score, diary_restaurant_id, diary_user_id = [], [], [], []
        for diary_date in diary_date_list:  # 2022-06-01 ~ 2022-06-30
            ok = False
            # DB에 있는지 체크
            for re in results:
                # print('===sibal==', diary_date, type(diary_date), re.diary_date, type(re.diary_date))
                if re.diary_date == diary_date:
                    diary_id.append(re.id)
                    diary_score.append(re.diary_score)
                    diary_restaurant_id.append(re.diary_restaurant_id)
                    diary_user_id.append(re.diary_user_id)
                    ok = True
                    break
                else:
                    continue
            if ok == False:  # 만약 DB에 없는 거면.
                diary_id.append(None)
                diary_score.append(None)
                diary_restaurant_id.append(None)
                diary_user_id.append(None)
        is_diary_list = [False if ds == None else True for ds in diary_score]
        days = ['월', '화', '수', '목', '금', '토', '일']
        diary_weekday_list = list(map(lambda x: days[x.weekday()] if x != '' else '', diary_date_list))
        diary_date_list = list(map(lambda x: datetime.strftime(x, '%Y-%m-%d') if x != '' else '',
                                   diary_date_list))  # datetime.date to string

        # id명 : 가게명 / dictionary {}
        interchange_name_id = {data.id: data.restaurant_name for data in
                               Restaurant.objects.filter().only('restaurant_name')}
        diary_restaurant_name = []
        for id in diary_restaurant_id:
            try:
                diary_restaurant_name.append(interchange_name_id[id])
            except:
                diary_restaurant_name.append(None)

        print('================')
        print('date_list :', date_list, len(date_list))  # ' ',' ', '1', '2' ... '31'
        print('is_date_list :', is_date_list, len(is_date_list))  # True, False
        print('diary_id :', diary_id, len(diary_id))  # [1, 2, 3, 4]
        print('diary_weekday_list:', diary_weekday_list, len(diary_weekday_list))  # ['수','목','금'...]
        print('diary_date_list :', diary_date_list,
              len(diary_date_list))  # ['2022-06-02', '2022-06-03'... '2022-06-30']
        print('diary_score :', diary_score, len(diary_score))  # [3, 4, 5, 2, 1, ...]
        print('is_diary_list :', is_diary_list, len(is_diary_list))  # by score [True, False, False ...]
        print('diary_restaurant_id :', diary_restaurant_id, len(diary_restaurant_id))  # [37, 25, 131, 86 ...]
        print('diary_restaurant_name : ', diary_restaurant_name, len(diary_restaurant_name))  # ['두레반.', '봉추찜닭'..]
        print('diary_user_id :', diary_user_id, len(diary_user_id))  # [1,1,1,1,2,2,2]
        print('=================')

        result_date_list = []
        for day, is_day, id, date, weekday, is_diary, score, restaurant_id, restaurant_name \
                in zip(date_list, is_date_list, diary_id, diary_date_list, diary_weekday_list, \
                       is_diary_list, diary_score, diary_restaurant_id, diary_restaurant_name):
            result_date_list.append(
                {
                    'day': day,
                    'is_date': is_day,
                    'id': id,
                    'date': date,  # 2022-06-17,
                    'weekday': weekday,  # '월'
                    'is_diary': is_diary,
                    'restaurant_score': score,
                    'restaurant_id': restaurant_id,
                    'restaurant_name': restaurant_name
                }
            )

        print('====최종 dict===', result_date_list[3])
        print('====최종 dict===', result_date_list[7])

        # 한 주씩 끊어서. 35개 => 5x7로
        final_results = []
        for m in range(1, 6):
            final_results.append(result_date_list[0 + (7 * (m - 1)):7 * m])

        # 가게 이름 list        
        resturant_name_list = [val for _, val in interchange_name_id.items()]
        # .itemslist(map(lambda x : x.restaurant_name, Restaurant.objects.filter().only('restaurant_name')))
        # print('=====', resturant_name_list, len(resturant_name_list))
        return render(request, 'mypage/mypage.html', {'calendar': final_results, 'year': year, 'month': month,
                                                      'resturant_name_list': resturant_name_list})


def create_diary(request):
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
            print('=== 해당 유저는 해당 음식점을 평가하는 것이 ', diary_star.star_count, '번째 입니다. ')
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


def update_diary(request):
    if request.method == 'PATCH':
        data = json.loads(request.body)
        date = datetime.strptime(data['date_val'], '%Y-%m-%d').date()  # data['weekday_val'] : 요일
        restaurant_name = data['search_val']
        after_diary_score = int(data['score_val'])
        user_id = request.user.id

        # before_star = Star.objects.get(star_restaurant_id=diary_restaurant_id, star_user_id=user_id)
        before_diary = Diary.objects.get(diary_date=date, diary_user_id=user_id)
        before_diary_score = before_diary.diary_score

        # Restaurant
        before_restaurant_id = before_diary.diary_restaurant_id
        before_restaurant = Restaurant.objects.get(id=before_restaurant_id)
        before_restaurant_count = before_restaurant.restaurant_count
        before_restaurant_score = before_restaurant.restaurant_avg_score

        after_restaurant = Restaurant.objects.get(restaurant_name=restaurant_name)
        after_restaurant_id = after_restaurant.id
        after_restaurant_count = after_restaurant.restaurant_count
        after_restaurant_score = after_restaurant.restaurant_avg_score

        # Star
        before_star = Star.objects.get(star_restaurant_id=before_restaurant_id, star_user_id=user_id)
        before_star_id = before_star.id
        before_star_count = before_star.star_count
        before_star_score = before_star.star_avg_score

        ### Diary Table Create
        Diary.objects.filter(diary_user_id=user_id, diary_date=date) \
            .update(
            diary_restaurant=Restaurant.objects.get(restaurant_name=restaurant_name),
            diary_score=after_diary_score
        )

        ### Restaurant Table 값 Update
        # 1) Before
        # 1) Restaurant_name으로 조회
        # 2) Restaurant_Count는 그대로 유지
        # 3) 기존 스코어 찾아서 빼기
        # 4) Restaurant_Avg_score 재계산

        # 기존과 신규가 같을 때.
        if before_restaurant_id == after_restaurant_id:
            # avg_score만 update
            update_avg_score = ((
                                        before_restaurant_score * before_restaurant_count) - before_diary_score + after_diary_score) / before_restaurant_count
            Restaurant.objects.filter(restaurant_name=restaurant_name) \
                .update(
                restaurant_avg_score=update_avg_score
            )
        # 기존과 신규가 다를 때 => 기존건 무조건 빼주기(count) / 신규건 무조건 더해줌(score)
        else:
            before_update_count = before_restaurant_count - 1

            if (before_update_count) == 0:
                before_update_score = 0
            else:
                before_update_score = ((before_restaurant_score * before_restaurant_count) - before_diary_score) / (
                    before_update_count)
            Restaurant.objects.filter(id=before_restaurant_id) \
                .update(
                restaurant_count=before_update_count,
                restaurant_avg_score=before_update_score
            )

            after_update_count = after_restaurant_count + 1
            after_update_score = ((after_restaurant_score * after_restaurant_count) + after_diary_score) / (
                after_update_count)
            Restaurant.objects.filter(restaurant_name=restaurant_name) \
                .update(
                restaurant_count=after_update_count,
                restaurant_avg_score=after_update_score
            )

        ### Star Table 값 Create & Update
        # 0) Star Table은 User_id가 Restaurant_id를 평가한 정보 (Max Record 갯수 User_id * Restaurant_id)
        # 1) user id와 restaurant_id로 해당 정보에 접근
        # 2) if 카운트가 0이 아닌 경우 지금 코드
        # 3) elif 카운트가 0일 경우 생성 코드

        # 기존과 신규가 같을 때. (score만 바꾸려고 할 때)
        if before_restaurant_id == after_restaurant_id:
            # avg_score만 update
            update_avg_score = ((
                                            before_star_score * before_star_count) - before_diary_score + after_diary_score) / before_star_count
            Star.objects.filter(id=before_star_id) \
                .update(
                star_avg_score=update_avg_score
            )
        # 기존과 신규가 다를 때
        # 기존건 빼주기(count) + 0이 되면 행 삭제
        # 신규건 더해주기(count) + 없으면 생성.
        else:
            before_update_count = before_star_count - 1
            if before_update_count == 0:
                Star.objects.get(id=before_star_id).delete()
            else:
                update_avg_score = ((before_star_score * before_star_count) - before_diary_score) / before_update_count
                Star.objects.filter(id=before_star_id) \
                    .update(
                    star_count=before_update_count,
                    star_avg_score=update_avg_score
                )

            try:
                after_star = Star.objects.get(star_restaurant_id=after_restaurant_id, star_user_id=user_id)
                after_star_id = after_star.id
                after_star_count = after_star.star_count
                after_star_score = after_star.star_avg_score

            except:
                after_star = None
            # 객체가 있으면 단순 더해주기
            if after_star != None:
                after_update_count = after_star_count + 1
                after_update_score = ((after_star_score * after_star_count) + after_diary_score) / after_update_count
                Star.objects.filter(id=after_star_id) \
                    .update(
                    star_count=after_update_count,
                    star_avg_score=after_update_score
                )

            # 객체가 없으면 생성하기
            else:
                Star.objects.create(
                    star_date=datetime.strftime(datetime.today(), '%Y-%m-%d'),  # last update date
                    star_avg_score=after_diary_score,
                    star_count=1,
                    star_restaurant_id=after_restaurant_id,
                    star_user_id=user_id
                )

        return JsonResponse({'msg': 'Diary 수정 완료!'})


def delete_diary(request):
    if request.method == 'DELETE':
        data = json.loads(request.body)
        date = datetime.strptime(data['date_val'], '%Y-%m-%d').date()  # data['weekday_val'] : 요일
        restaurant_name = data['search_val']
        user_id = request.user.id

        ### Delete Diary
        delete_diary = Diary.objects.get(diary_user_id=user_id, diary_date=date)
        delete_diary.delete()

        ### Delete Restaurant
        # 해당 가게 정보 (count, score) 감소만
        delete_diary_score = delete_diary.diary_score
        delete_restaurant_id = delete_diary.diary_restaurant_id

        delete_restaurant = Restaurant.objects.get(id=delete_restaurant_id)
        delete_restaurant_score = delete_restaurant.restaurant_avg_score
        delete_restaurant_count = delete_restaurant.restaurant_count

        # 값 빼주고 Update
        update_restaurant_count = delete_restaurant_count - 1
        if update_restaurant_count == 0:
            update_restaurant_score = 0
        else:
            update_restaurant_score = ((
                                                   delete_restaurant_score * delete_restaurant_count) - delete_diary_score) / update_restaurant_count

        Restaurant.objects.filter(id=delete_restaurant_id) \
            .update(
            restaurant_count=update_restaurant_count,
            restaurant_avg_score=update_restaurant_score
        )

        ### Delete Star
        # 해당 Star 정보 (count, score) 감소 + 0이면 삭제
        delete_star = Star.objects.get(star_restaurant_id=delete_restaurant_id, star_user_id=user_id)
        delete_star_id = delete_star.id
        delete_star_score = delete_star.star_avg_score
        delete_star_count = delete_star.star_count

        # 값 빼주고 update, delete
        update_star_count = delete_star_count - 1
        if update_star_count == 0:  # delete
            delete_star.delete()
        else:  # update
            update_star_score = ((delete_star_score * delete_star_count) - delete_diary_score) / update_star_count
            Star.objects.filter(id=delete_star_id) \
                .update(
                star_count=update_star_count,
                star_avg_score=update_star_score
            )
        return JsonResponse({'msg': 'Diary 삭제 완료!'})
