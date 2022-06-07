import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
# print('==추가한 Path:', os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from django.db import models
from restaurant import models as restaurantmodels
from users import models as usermodels


# Create your models here.
class star(models.Model):
    star_score = models.FloatField()
    star_date = models.DateField(auto_now=False)
    star_restaurant = models.ForeignKey(restaurantmodels.Restaurant, on_delete=models.CASCADE)
    star_user = models.ForeignKey(usermodels.UserModel, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Star'
