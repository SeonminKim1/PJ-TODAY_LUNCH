import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
# print('==추가한 Path:', os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from django.db import models
from restaurant.models import Restaurant
from users.models import UserModel
# Create your models here.

class Diary(models.Model):
    # date, restaurant_id, score
    diary_date = models.DateField(auto_now=False)
    diary_user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    diary_restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    diary_score = models.IntegerField(default=0)

    class Meta:
        db_table = 'Diary'