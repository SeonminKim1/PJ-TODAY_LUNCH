from django.shortcuts import render

# Create your views here.

def mypage_view(request):
    if request.method=='GET':
        return render(request, 'mypage/mypage.html')