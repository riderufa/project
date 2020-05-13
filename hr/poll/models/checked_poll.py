from django.db import models

class CheckedPoll(models.Model):
    """
    Пройденный опрос
    """
    poll = models.ForeignKey('Poll', on_delete=models.SET_NULL, null=True, verbose_name='опрос', related_name='checked_poll') # Ссылка на родительский опрос
    user = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='user_checked_polls', verbose_name='пользователь', null=True) # Ссылка на привязанного пользователя
    checked = models.BooleanField(null=True, blank=True) # Пройденный опрос
    valid = models.BooleanField(null=True, blank=True) # Правильно пройденный опрос
    rank = models.IntegerField(null=True, blank=True) # Полученный балл за опрос
    validated = models.BooleanField(null=True, blank=True, default=False) # Опрос, прошедший проверку на программные ошибки

    def __str__(self):
        return self.poll.name