from django.db import models
from ..restaurant import models as restaurantmodels
from ..users import models as usermodels

# Create your models here.
class star(models.Model):
    score = models.FloatField()
    date = models.DateField(auto_now=False)
    restaurant_name = models.ForeignKey(restaurantmodels.Restaurant, on_delete=models.CASCADE)
    user_name = models.ForeignKey(usermodels.UserModel, on_delete=models.CASCADE)

    
    def __str__(self):
        return self.restaurant_name

    class Meta:
        db_table = 'Star'
