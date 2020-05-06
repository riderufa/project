from django.db import models

# Create your models here.
class CheckedAnswer(models.Model):

    text = models.TextField('текст ответа')
    checked = models.BooleanField('валидность ответа')
    question = models.ForeignKey('CheckedQuestion', on_delete=models.CASCADE, related_name='answers')
    
    def __str__(self):
        return self.text

    