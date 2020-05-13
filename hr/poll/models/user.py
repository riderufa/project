from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):  
    """
    Профиль пользователя
    """
    class TypeOfUser(models.IntegerChoices):
        MANAGER = 1
        USER = 2

    user = models.OneToOneField(User, on_delete=models.CASCADE) # Ссылка на класс User
    type_user = models.IntegerField('тип пользователя', choices=TypeOfUser.choices, null=True, blank=True) # Тип пользователя
    age = models.IntegerField('возраст') # Возраст

    def __str__(self):
        return self.user.username