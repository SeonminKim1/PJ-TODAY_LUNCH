from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import UserModel
from django.contrib import auth # 사용자 auth 기능
from django.contrib.auth.decorators import login_required

from datetime import datetime

# Join
def join_view(request):
    # Page View
    if request.method == 'GET':
        return render(request, 'users/join.html')

    # Page POST
    elif request.method == 'POST':
        user_email = request.POST.get('user_email', ' ')
        user_name = request.POST.get('user_name', ' ')
        password = request.POST.get('password', ' ')
        address = request.POST.get('address', ' ')
        gender = request.POST.get('gender', ' ')
        birthdate = request.POST.get('birthdate', ' ')
        
        date_format = '%y%m%d'
        birthdate = datetime.strptime(birthdate, date_format).date()        
        
        print(user_email, user_name, password, address, gender, birthdate)
        user_model = UserModel()
        user_model.email = user_email
        user_model.username = user_name
        user_model.password = password
        user_model.address = address
        user_model.gender = gender
        user_model.birthdate = birthdate
        user_model.save()

        return redirect('login')  # 회원가입이 완료되었으므로 로그인 페이지로 이동

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('user_name', "")
        password = request.POST.get('password', "")

        # 저장된 사용자의 패스워드와 입력받은 패스워드 비교
        me = auth.authenticate(request, username=username, password=password)
        if me is not None:  
            auth.login(request, me)
            return redirect('main')
        else:
            return render(request,'users/login.html')  # 로그인 실패

    elif request.method == 'GET':
        user = request.user.is_authenticated  # 사용자가 로그인 되어 있는지 검사
        if user:  # 로그인이 되어 있다면
            return redirect('main')
        else:  # 로그인이 되어 있지 않다면
            return render(request, 'users/login.html')

@login_required # 로그인 한 사용자만 함수 호출 가능
def logout(request):
    auth.logout(request) # 인증 되어있는 정보를 없애기
    return redirect("/")

def init_view(request):
    return render(request, 'init/init.html')

def main_view(request):
    return render(request, 'main/main.html')