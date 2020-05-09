from django.db import models
from PIL import Image

# from PIL import image

# Create your models here.
class Question(models.Model):

    class TypeOfQuestion(models.IntegerChoices):
        MONO = 1
        MULTI = 2

    text = models.TextField('текст вопроса')
    type = models.IntegerField('тип вопроса', choices=TypeOfQuestion.choices)
    image = models.ImageField(upload_to='images/%Y/%m/%d', null=True, blank=True, verbose_name='изображение')
    time_limit = models.IntegerField('предельное время (сек)', null=True, blank=True)
    # answers = models.ManyToManyField('Answer', related_name='question')
    checked_count = models.IntegerField(null=True, blank=True)
    valid_count = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.text

    def save(self):
        super().save()
        
        if self.image:
            img = Image.open(self.image.path)
            if img.height > 200 or img.width > 200:
                output_size = (200, 200)
                img.thumbnail(output_size)
                img.save(self.image.path)