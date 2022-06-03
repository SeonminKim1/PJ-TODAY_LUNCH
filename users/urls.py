from django.urls import path
from . import views

urlpatterns = [
    path('', views.init_view, name='init'),
    path('main/', views.main_view, name='main'),
    path('join/', views.join_view, name='join'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout, name='logout')
]