from django.db import models

class Poll(models.Model):
    """
    Опрос
    """
    name = models.CharField(max_length=50, verbose_name='наименование опроса') # Наименоваие опроса
    time_limit = models.IntegerField(null=True, blank=True, verbose_name='предельное время (сек)') # Лимит времени на весь опрос
    date_pub = models.DateField(verbose_name='дата публикации') # Дата публикации опроса
    questions = models.ManyToManyField('Question', through='Kit', through_fields=('poll', 'question'), related_name='polls', verbose_name='Список вопросов', blank=True) # Список вопросов в опросе
    admin = models.ForeignKey('UserProfile', on_delete=models.PROTECT, related_name='admin_polls', verbose_name='администратор', null=True) # Администратор опроса
    user = models.ManyToManyField('UserProfile', related_name='user_polls', verbose_name='пользователь', blank=True) # Список назначенных пользователей
    test = models.BooleanField(null=True, blank=True) # Опрос или тест
    checked_count = models.IntegerField(null=True, blank=True) # Количество пройденных опросов
    valid_count = models.IntegerField(null=True, blank=True) # Колчество правильно пройденных опросов
    rank = models.IntegerField(null=True, blank=True) # Общий балл за опрос
    
    def __str__(self):
        return self.name