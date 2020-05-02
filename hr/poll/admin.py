from django.contrib import admin
from .models import Question, Answer, UserProfile, Poll, Kit

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    fields = ['text_question', 'type_question', 'image_question', 'time_limit_question', 'answers_question']

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    fields = ['text_answer', 'valid_answer']

@admin.register(UserProfile)  
class ProfileAdmin(admin.ModelAdmin):  
    fields = ['user', 'type_user', 'age']


class KitAdmin(admin.TabularInline):  
    model = Poll.questions.through

@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    fields = ['name', 'time_limit', 'date_pub', 'user']
    inlines = (KitAdmin,)
