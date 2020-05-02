from django.db import models

# Create your models here.
class Answer(models.Model):

    text_answer = models.TextField('текст ответа')
    valid_answer = models.BooleanField('валидность ответа')

    def __str__(self):
        return self.text_answer