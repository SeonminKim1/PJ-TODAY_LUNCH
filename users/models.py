from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class UserModel(AbstractUser):
    class Meta:
        db_table = "my_user"

    def __str__(self):
        return self.username

    GENDER_CHOICE = (
        ('M', '남성(Man)'),
        ('W', '여성(Woman)'),
    )

    user_address = models.CharField(max_length=256, null=False, verbose_name='주소')
    user_gender = models.CharField(max_length=1, choices=GENDER_CHOICE, verbose_name='성별')
    user_birthdate = models.DateField(verbose_name='생년월일')