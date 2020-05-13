from django.db import models
from PIL import Image


class Question(models.Model):
    """
    Вопрос
    """
    class TypeOfQuestion(models.IntegerChoices):
        MONO = 1
        MULTI = 2

    text = models.CharField(max_length=150, verbose_name='текст вопроса') # Текст вопроса
    type = models.IntegerField('тип вопроса', choices=TypeOfQuestion.choices) # Тип вопроса по количеству ответов на вопрос
    image = models.ImageField(upload_to='images/%Y/%m/%d', null=True, blank=True, verbose_name='изображение') # Изображение к вопросу
    time_limit = models.IntegerField('предельное время (сек)', null=True, blank=True) # Лимит времени на вопрос
    checked_count = models.IntegerField(null=True, blank=True) # Количество вопросов, на которые получен ответ
    valid_count = models.IntegerField(null=True, blank=True) # Количество вопросов, на которые получен ответ правильно

    def __str__(self):
        return self.text

    # Изменяем размер изображения для сохранения
    def save(self):
        super().save()
        
        if self.image:
            img = Image.open(self.image.path)
            if img.height > 200 or img.width > 200:
                output_size = (200, 200)
                img.thumbnail(output_size)
                img.save(self.image.path)