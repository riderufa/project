from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):  

    class TypeOfUser(models.IntegerChoices):
        MANAGER = 1
        USER = 2

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    type_user = models.IntegerField('тип пользователя', choices=TypeOfUser.choices)
    age = models.IntegerField('возраст') 

    def __str__(self):
        return self.user.username