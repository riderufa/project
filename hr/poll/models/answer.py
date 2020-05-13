from django.db import models

class Answer(models.Model):
    """
    Ответ на вопрос
    """
    text = models.CharField(max_length=150, verbose_name='текст ответа') # Текст ответа
    valid = models.BooleanField(verbose_name='валидность ответа') # Валидность ответа
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='answers', verbose_name='Вопрос') # Ссылка еа вопрос
    checked_count = models.IntegerField(null=True, blank=True, verbose_name='Количество отмеченных') # Количество отмеченных ответов
    valid_count = models.IntegerField(null=True, blank=True, verbose_name='Количество отмеченных верно') # Количество верно отмеченных ответов

    def __str__(self):
        return self.text