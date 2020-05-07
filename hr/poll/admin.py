from django.contrib import admin
from .models import Question, Answer, UserProfile, Poll, Kit, CheckedPoll, CheckedQuestion, CheckedAnswer

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    fields = ['text', 'type', 'image', 'time_limit', 'kit']

@admin.register(Kit)
class KitAdmin(admin.ModelAdmin):
    fields = ['poll', 'question', 'rank']


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    fields = ['text', 'valid', 'question']

@admin.register(UserProfile)  
class ProfileAdmin(admin.ModelAdmin):  
    fields = ['user', 'type_user', 'age']


class KitAdmin(admin.TabularInline):  
    model = Poll.questions.through

@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    fields = ['name', 'time_limit', 'date_pub', 'user', 'admin']
    inlines = (KitAdmin,)

@admin.register(CheckedPoll)
class CheckedPollAdmin(admin.ModelAdmin):
    fields = ['poll', 'user']

@admin.register(CheckedQuestion)
class CheckedQuestionAdmin(admin.ModelAdmin):
    fields = ['poll', 'question']

@admin.register(CheckedAnswer)
class CheckedAnswerAdmin(admin.ModelAdmin):
    fields = ['answer', 'valid', 'question']
