from django.db import models

class Kit(models.Model):

    poll = models.ForeignKey('Poll', on_delete=models.CASCADE, related_name='kitpoll')
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='kitquestion')
    rank = models.IntegerField()

    def __str__(self):
        return self.poll.name