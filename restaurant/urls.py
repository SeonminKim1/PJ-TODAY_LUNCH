from django.urls import path
from restaurant import views

urlpatterns = [
    path('res_info/<int:restaurant_id>', views.info, name='info')
]
