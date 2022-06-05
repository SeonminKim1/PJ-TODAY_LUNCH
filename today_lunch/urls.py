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
from users import views as userview
from restaurant import views as resview
#    path('', include('user.urls')), # user앱의 urls.py와 연결
#    path('', include('tweet.urls')), # tweet 앱의 urls.py와 연결

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include('restaurant.urls')),
    # init
    path('', userview.init_view, name='init'),
    
    # user - join, login, logout
    path('user/join/', userview.join_view, name='join'),
    path('user/login/', userview.login_view, name='login'),
    path('user/logout/', userview.logout, name='logout'),

    # register 2
    # path('main/', resview.main_view, name='main'),
    path('res_view/<int:restaurant_id>', resview.res_view, name='res_view'),
    path('basic_view/', resview.basic_view, name='basicview'),
    path('basic_view/put_score/', resview.put_score, name='put_score'),
    path('basic_view/main/', resview.main_view, name='mainview'),

    # main
    path('main/', resview.main_view, name='main' ),
]