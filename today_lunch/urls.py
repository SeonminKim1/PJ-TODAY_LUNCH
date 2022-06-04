"""join_login URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from users import views

#    path('', include('user.urls')), # user앱의 urls.py와 연결
#    path('', include('tweet.urls')), # tweet 앱의 urls.py와 연결

urlpatterns = [
    path('admin/', admin.site.urls),
    # init
    path('', views.init_view, name='init'),
    
    # user - join, login, logout
    path('user/join/', views.join_view, name='join'),
    path('user/login/', views.login_view, name='login'),
    path('user/logout/', views.logout, name='logout'),

    # main
    path('main/', views.main_view, name='main'),
]
