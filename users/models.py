from django.db import models
from django.contrib.auth.models import AbstractUser

class UserModel(AbstractUser):
    class Meta:
        db_table = "USERS"

    def __str__(self):
        return self.username

    GENDER_CHOICE = (
        ('M', '남성(Man)'),
        ('W', '여성(Woman)'),
    )
    # address, gender, birthdate
    address = models.CharField(max_length=256, null=False, verbose_name='주소')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICE, verbose_name='성별')
    birthdate = models.DateField(auto_now=False, verbose_name='생년월일')
