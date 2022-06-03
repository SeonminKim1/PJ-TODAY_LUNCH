from django.db import models
from django.contrib.auth.models import AbstractUser

class UserModel(AbstractUser):
    # address, gender, birthdate
    address = models.CharField(max_length=256)
    gender = models.CharField(max_length=10)
    birthdate = models.DateField(auto_now=False)