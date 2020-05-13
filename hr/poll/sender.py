from .models import Poll

# Сигнал на подсчет общего количества баллов опроса при создании или изменении количества баллов за вопрос
def post_save_kit(sender, **kwargs):
    poll = Poll.objects.get(pk=kwargs['instance'].poll.pk)
    poll_rank = 0
    for kit in poll.kitpoll.all():
        poll_rank += kit.rank
    poll.rank = poll_rank
    poll.save()

# Сигнал на подсчет общего количества баллов опроса при удалении вопроса из опроса
def post_delete_kit(sender, **kwargs):
    poll = Poll.objects.get(pk=kwargs['instance'].poll.pk)
    poll_rank = 0
    for kit in poll.kitpoll.all():
        poll_rank += kit.rank
    poll.rank = poll_rank
    poll.save()