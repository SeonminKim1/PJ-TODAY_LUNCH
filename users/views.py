from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import UserModel
from django.contrib import auth # 사용자 auth 기능
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from datetime import datetime

def init_view(request):
    return render(request, 'init/init.html')

# Join
def join_view(request):
    # Page View
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return redirect("/")
        else:
            return render(request, 'users/join.html')

    # Page POST
    elif request.method == 'POST':
        user_email = request.POST.get('user_email', ' ')
        user_name = request.POST.get('user_name', ' ')
        password = request.POST.get('password', ' ')
        password2 = request.POST.get('password2', '')
        address = request.POST.get('address', ' ')
        address_detil = request.POST.get('address_detil', ' ')
        
        gender = request.POST.get('gender', ' ')
        birthdate = request.POST.get('birthdate', ' ')

        final_address = address + ' ' + address_detil
        birthdate = datetime.strptime(birthdate, '%y%m%d').date() 
        print(user_email, user_name, password, final_address, gender, birthdate)

        if password != password2:
            return render(request, 'users/join.html', {'error': '패스워드를 확인 해 주세요!'})
        else:
            if user_email == '' or password == '':
                # 사용자 저장을 위한 username과 password가 필수라는 것을 얘기 해 줍니다.
                return render(request, 'users/join.html', {'error': '사용자 아이디와 패스워드는 필수 값 입니다'})

            exist_user = get_user_model().objects.filter(email=user_email)
            if exist_user:
                return render(request, 'users/join.html', {'error':'이미 가입된 이메일입니다.'})  # 사용자가 존재하기 때문에 사용자를 저장하지 않고 회원가입 페이지를 다시 띄움
            else:
                UserModel.objects.create_user(
                    email=user_email, username=user_name, 
                    password=password, address=final_address,
                    gender=gender, birthdate=birthdate)
                print('회원가입이 정상적으로 완료 되었습니다~')
                return redirect('login')  # 회원가입이 완료되었으므로 로그인 페이지로 이동

def login_view(request):
    if request.method == 'POST':
        user_email = request.POST.get('user_email', "")
        password = request.POST.get('password', "")

        print('===', user_email, password)
        # 저장된 사용자의 패스워드와 입력받은 패스워드 비교
        # 여기 auth.authenticate 제대로 작동안하는 오류있습니다.
        me = auth.authenticate(request, email=user_email, password=password)
        print('me', me)
        if me is not None:  
            auth.login(request, me)
            return redirect('main')
        else:
            print(1)
            return render(request,'users/login.html', {'error':'유저이름 혹은 패스워드를 확인 해 주세요'})  # 로그인 실패

    elif request.method == 'GET':
        user = request.user.is_authenticated  # 사용자가 로그인 되어 있는지 검사
        if user:  # 로그인이 되어 있다면
            return redirect('main')
        else:  # 로그인이 되어 있지 않다면
            print(2)

            return render(request, 'users/login.html')

@login_required # 로그인 한 사용자만 함수 호출 가능
def logout(request):
    auth.logout(request) # 인증 되어있는 정보를 없애기
    return redirect("/")

def main_view(request):
    return render(request, 'main/main.html')
