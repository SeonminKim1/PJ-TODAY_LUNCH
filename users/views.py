from django.shortcuts import render, redirect
from .models import UserModel
from django.contrib import auth  # 사용자 auth 기능
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.http import HttpResponse

def init_view(request):
    if request.method == 'GET':
        user = request.user.is_authenticated  # 사용자가 로그인 되어 있는지 검사
        if user:  # 로그인이 되어 있다면
            auth.logout(request)
            return render(request, 'init/init.html')
        else:  # 로그인이 되어 있지 않다면
            return render(request, 'init/init.html')


# Join
def join_view(request):
    # Page View
    if request.method == 'GET':
        return render(request, 'users/join.html')

    # Page POST
    elif request.method == 'POST':
        user_email = request.POST.get('user_email', '')
        user_name = request.POST.get('user_name', '')
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        address = request.POST.get('address', '')
        address_detail = request.POST.get('address_detail', '')

        gender = request.POST.get('gender', '')  # 'M' , 'W'
        birthdate = request.POST.get('birthdate', '')  # 940526

        # validation 1 ) user email, password 잘 들어왔는지.
        if user_email == '' or password == '' or password2 == '' or user_name == '' or address == '' or gender == '' or birthdate == '':
            messages.error(request, '회원가입 정보를 모두 기입해주세요.')
            return render(request, 'users/join.html', {'error': '회원가입 정보를 모두 기입해주세요.'})

        # validation 2 ) 가입된 이메일인지
        exist_user = get_user_model().objects.filter(email=user_email)
        if exist_user:
            messages.error(request, '이미 가입된 이메일 입니다.')
            return render(request, 'users/join.html', {'error': '이미 가입된 이메일입니다.'})

        # validation 3 ) password 중복체크
        if password != password2:
            messages.error(request, '패스워드가 서로 다릅니다. 패스워드를 확인해 주세요!')
            return render(request, 'users/join.html', {'error': '패스워드를 확인 해 주세요!'})

        # validation 4) 생년월일 6자리인지
        if len(birthdate.strip()) != 6:
            messages.error(request, '생년월일을 형식에 맞춰 작성해 주세요!')
            return render(request, 'users/join.html', {'error': '생년월일을 형식에 맞춰 작성해 주세요!'})

        # Process Data
        final_address = address + ', ' + address_detail
        birthdate = datetime.strptime(birthdate, '%y%m%d').date()

        print(user_email, user_name, password, final_address, gender, birthdate)
        # 모든 validation 통과~
        UserModel.objects.create_user(
            email=user_email, username=user_email, fullname=user_name,
            password=password, address=final_address,
            gender=gender, birthdate=birthdate)

        messages.success(request, '회원가입이 정상적으로 완료 되었습니다')
        print('회원가입이 정상적으로 완료 되었습니다~')
        return redirect('login')  # 회원가입이 완료되었으므로 로그인 페이지로 이동


def login_view(request):
    # Login page
    if request.method == 'GET':
        user = request.user.is_authenticated  # 사용자가 로그인 되어 있는지 검사
        if user:  # 로그인이 되어 있다면
            return redirect('scoring_view')
        else:  # 로그인이 되어 있지 않다면
            return render(request, 'users/login.html')
    # Login Button - Click
    elif request.method == 'POST':
        user_email = request.POST.get('user_email', "")
        password = request.POST.get('password', "")

        # validation 1) username과 password 비교
        me = auth.authenticate(request, username=user_email, password=password)  # me 정상시 username이 됨.
        if me is not None:
            auth.login(request, me)
            # messages.success(request, '로그인 성공!')
            return redirect('scoring_view')
        else:  # 로그인 인증 실패
            messages.error(request, '로그인 실패! 아이디 or 패스워드를 확인 해 주세요!')
            return render(request, 'users/login.html', {'error': '로그인 실패! 아이디 or 패스워드를 확인 해 주세요!'})  # 로그인 실패


@login_required  # 로그인 한 사용자만 함수 호출 가능
def logout(request):
    auth.logout(request)  # 인증 되어있는 정보를 없애기
    messages.success(request, '로그아웃 성공!')
    return redirect("/")
