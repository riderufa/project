from django.db import models

class Poll(models.Model):

    name = models.CharField(max_length=50, verbose_name='наименование опроса')
    time_limit = models.IntegerField(null=True, blank=True, verbose_name='предельное время (сек)')
    date_pub = models.DateField(verbose_name='дата публикации')
    questions = models.ManyToManyField('Question', through='Kit', through_fields=('poll', 'question'), related_name='polls', verbose_name='Список вопросов')
    user = models.ForeignKey('UserProfile', on_delete=models.PROTECT, related_name='user_polls', verbose_name='пользователь')

    def __str__(self):
        return self.name