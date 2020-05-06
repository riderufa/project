from django.db import models

# Create your models here.
class CheckedQuestion(models.Model):

    question = models.ForeignKey('Question', on_delete=models.SET_NULL, verbose_name='вопрос', null=True)
    # user = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    poll = models.ForeignKey('CheckedPoll', on_delete=models.CASCADE, related_name='questions')
    # score = models.IntegerField()
    # image = models.ImageField(upload_to='images/%Y/%m/%d', null=True, blank=True, verbose_name='изображение')
    # time_limit = models.IntegerField('предельное время (сек)', null=True, blank=True)
    # answers = models.ManyToManyField('Answer', related_name='question')

    def __str__(self):
        return self.question.text

    