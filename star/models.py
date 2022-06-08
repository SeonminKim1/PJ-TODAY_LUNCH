import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
# print('==추가한 Path:', os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from django.db import models
from restaurant.models import Restaurant
from users.models import UserModel

class Star(models.Model):
    star_date = models.DateField(auto_now=False)
    star_restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    star_user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    star_avg_score = models.FloatField()

    class Meta:
        db_table = 'Star'
