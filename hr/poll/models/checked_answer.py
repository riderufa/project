from django.db import models

# Create your models here.
class CheckedAnswer(models.Model):

    # text = models.TextField('текст ответа', null=True, blank=True)
    # checked = models.BooleanField('валидность ответа', null=True, blank=True)
    answer = models.ForeignKey('Answer', on_delete=models.CASCADE, related_name='checked_anwers', null=True, blank=True)
    valid = models.BooleanField(null=True, blank=True)
    question = models.ForeignKey('CheckedQuestion', on_delete=models.CASCADE, related_name='answers', null=True, blank=True)
    
    def __str__(self):
        return self.answer.text

    