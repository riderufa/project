from django.db import models

class CheckedQuestion(models.Model):
    """
    Вопрос, на который получен ответ
    """
    question = models.ForeignKey('Question', on_delete=models.SET_NULL, verbose_name='вопрос', null=True, related_name='checked_questions') # Ссылка на родительский вопрос
    poll = models.ForeignKey('CheckedPoll', on_delete=models.CASCADE, related_name='questions') # Ссылка на пройденный опрос
    valid = models.BooleanField(null=True, blank=True) # Валидность ответа
    rank = models.IntegerField(null=True, blank=True) # Полученный балл

    def __str__(self):
        return self.question.text
