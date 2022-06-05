from django.urls import path
from restaurant import views

urlpatterns = [
    path('res_view/<int:restaurant_id>', views.res_view, name='res_view')
]
