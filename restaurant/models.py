from django.db import models

# Create your models here.
class Categories(models.Model):
    restaurant_category = models.CharField(max_length=45)

    def __str__(self):
        return self.restaurant_category

    class Meta:
        db_table = 'Categories'


class Restaurant(models.Model):
    restaurant_name = models.CharField(max_length=45)
    restaurant_address = models.TextField()
    restaurant_image = models.TextField()
    restaurant_category = models.ForeignKey(Categories, on_delete=models.CASCADE)

    def __str__(self):
        return self.restaurant_name

    class Meta:
        db_table = 'Restaurant'