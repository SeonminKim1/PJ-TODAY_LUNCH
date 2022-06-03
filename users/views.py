from django.shortcuts import render, redirect, HttpResponse
from .models import UserModel
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

def init_view(request):
    return render(request, 'init/init.html')

def join_view(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return redirect("/")
        else:
            return render(request, 'users/signup.html')
    elif request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        user_address = request.POST.get('user_address', '')
        user_gender = request.POST.get('user_gender', '')
        user_birthdate = request.POST.get('user_birthdate', '')

        if password != password2:
            return render(request, 'users/signup.html', {'error': '패스워드를 확인 해 주세요!'})
        else:
            if username == '' or password == '':
                # 사용자 저장을 위한 username과 password가 필수라는 것을 얘기 해 줍니다.
                return render(request, 'users/signup.html', {'error': '사용자 이름과 패스워드는 필수 값 입니다'})

            exist_user = get_user_model().objects.filter(username=username)
            if exist_user:
                return render(request, 'users/signup.html', {'error':'사용자가 존재합니다.'})  # 사용자가 존재하기 때문에 사용자를 저장하지 않고 회원가입 페이지를 다시 띄움
            else:
                UserModel.objects.create_user(username=username, password=password, user_address=user_address, user_gender=user_gender, user_birthdate=user_birthdate)
                return redirect('/login')  # 회원가입이 완료되었으므로 로그인 페이지로 이동


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', "")
        password = request.POST.get('password', "")

        me = auth.authenticate(request, username=username, password=password)  # 사용자 불러오기
        if me is not None:  # 저장된 사용자의 패스워드와 입력받은 패스워드 비교
            auth.login(request, me)
            return redirect('/main')
        else:
            return render(request,'users/signin.html',{'error':'유저이름 혹은 패스워드를 확인 해 주세요'})  # 로그인 실패
    elif request.method == 'GET':
        user = request.user.is_authenticated  # 사용자가 로그인 되어 있는지 검사
        if user:  # 로그인이 되어 있다면
            return redirect('/main')
        else:  # 로그인이 되어 있지 않다면
            return render(request, 'users/signin.html')

@login_required
def main_view(request):
    return render(request, 'main/main.html')

@login_required
def logout(request):
    auth.logout(request)
    return redirect("/")