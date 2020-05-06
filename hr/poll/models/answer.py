from django.db import models

# Create your models here.
class Answer(models.Model):

    text = models.TextField('текст ответа')
    valid = models.BooleanField('валидность ответа')
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='answers')

    def __str__(self):
        return self.text