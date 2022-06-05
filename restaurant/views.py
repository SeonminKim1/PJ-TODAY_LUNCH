from django.shortcuts import render
from .models import Restaurant, Categories

# Create your views here.

def res_view(request, restaurant_id):
    if request.method == "GET":
        restaurant = Restaurant.objects.get(id=restaurant_id)
        return render(request, 'main/res_view.html', {'restaurant': restaurant})