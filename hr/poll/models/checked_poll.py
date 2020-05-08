from django.db import models

class CheckedPoll(models.Model):

    poll = models.ForeignKey('Poll', on_delete=models.SET_NULL, null=True, verbose_name='опрос')
    # admin = models.ForeignKey('UserProfile', on_delete=models.PROTECT, related_name='admin_checked_polls', verbose_name='администратор', null=True)
    # user = models.ManyToManyField('UserProfile', related_name='user_polls', verbose_name='пользователь', null=True, blank=True)
    user = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='user_checked_polls', verbose_name='пользователь', null=True)
    checked = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return self.poll.name