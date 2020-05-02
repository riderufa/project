from django.db import models

class Kit(models.Model):

    poll = models.ForeignKey('Poll', on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    rank = models.IntegerField()