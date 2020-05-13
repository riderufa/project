from django.db import models

class CheckedAnswer(models.Model):
    """
    Ответ на вопрос, на который получен ответ
    """
    answer = models.ForeignKey('Answer', on_delete=models.CASCADE, related_name='checked_answers', null=True, blank=True) # Ссылка на родительский ответ
    checked = models.BooleanField(null=True, blank=True) # Отмеченный ответ
    valid = models.BooleanField(null=True, blank=True) # Правильно отмеченный ответ
    question = models.ForeignKey('CheckedQuestion', on_delete=models.CASCADE, related_name='answers', null=True, blank=True) # Ссылка на вопрос, на который получен ответ
    
    def __str__(self):
        return self.answer.text

    