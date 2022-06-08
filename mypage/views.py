from django.shortcuts import render
from .models import Diary

from datetime import datetime     


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

        print('================')
        print(date_list, len(date_list))
        print(is_date_list, len(is_date_list))
        print(diary_id, len(diary_id))
        print(diary_date_list, len(diary_date_list))
        print(diary_score, len(diary_score))
        print(is_diary_list, len(is_diary_list))
        print(diary_restaurant_id, len(diary_restaurant_id))
        print(diary_user_id, len(diary_user_id))
        print('=================')

        result_date_list= []
        for day, is_day, id, date, is_diary, score, restaurant_id \
            in zip(date_list, is_date_list, diary_id, diary_date_list, is_diary_list, diary_score, diary_restaurant_id):
            result_date_list.append(
                {
                    'day': day,
                    'is_date':is_day,
                    'id': id,
                    'date': date, # datetime(year, month, day).date(),
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
        return render(request, 'mypage/mypage.html', {'date':final_results})