from django.db import models

class Kit(models.Model):
    """
    Таблица, связывающая опрос и вопрос с добавлением дополнительных полей
    """
    poll = models.ForeignKey('Poll', on_delete=models.CASCADE, related_name='kitpoll') # Ссылка на опрос
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='kitquestion') # Ссылка на вопрос
    rank = models.IntegerField() # Балл, получаемый за правильный ответ на вопрос в конкретном опросе

    def __str__(self):
        return self.poll.name