from django.db import models

# Create your models here.
class Question(models.Model):

    class TypeOfQuestion(models.IntegerChoices):
        MONO = 1
        MULTI = 2

    text = models.TextField('текст вопроса')
    type = models.IntegerField('тип вопроса', choices=TypeOfQuestion.choices)
    image = models.ImageField('изображение', null=True, blank=True)
    time_limit = models.IntegerField('предельное время (сек)', null=True, blank=True)
    answers = models.ManyToManyField('Answer', related_name='question')

    def __str__(self):
        return self.text