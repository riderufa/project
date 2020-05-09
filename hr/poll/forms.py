from datetime import date

from django import forms

from .models import UserProfile, Question, Poll, Answer, Kit, CheckedAnswer
  
  
class ProfileCreationForm(forms.ModelForm):  
  
    class Meta:  
        model = UserProfile  
        fields = ['age']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('text', 'type', 'image', 'time_limit')

# class PollForm(forms.ModelForm):
#     class Meta:
#         model = Poll
#         fields = ('name', 'date_pub', 'user', 'time_limit', 'questions')


class PollForm(forms.ModelForm):
    date_pub = forms.DateField(label='Дата публикации', widget=forms.SelectDateWidget())
    admin = forms.ModelChoiceField(label='Администратор', queryset=UserProfile.objects.all(), widget=forms.widgets.Select(attrs={'size': 1}), disabled=True)
    class Meta:
        model = Poll
        fields = ('name', 'date_pub', 'admin', 'time_limit', 'test')

class PollSetForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ('user',)


class AnswerForm(forms.ModelForm):
    question = forms.ModelChoiceField(label='Вопрос', queryset=Question.objects.all(), widget=forms.widgets.Select(attrs={'size': 1}), disabled=True)
    class Meta:
        model = Answer
        fields = ('text', 'valid', 'question')

class KitForm(forms.ModelForm):
    poll = forms.ModelChoiceField(label='Опрос', queryset=Poll.objects.all(), widget=forms.widgets.Select(attrs={'size': 1}), disabled=True)
    class Meta:
        model = Kit
        fields = ('poll', 'question', 'rank')

class KitEditForm(forms.ModelForm):
    poll = forms.ModelChoiceField(label='Опрос', queryset=Poll.objects.all(), widget=forms.widgets.Select(attrs={'size': 1}), disabled=True)
    question = forms.ModelChoiceField(label='Вопрос', queryset=Question.objects.all(), widget=forms.widgets.Select(attrs={'size': 1}), disabled=True)
    class Meta:
        model = Kit
        fields = ('poll', 'question', 'rank')

class UserQuestionForm(forms.Form):
    poll = forms.ModelChoiceField(label='Опрос', queryset=Poll.objects.all(), widget=forms.widgets.Select(attrs={'size': 1}))
    user = forms.ModelChoiceField(label='Пользователь', queryset=UserProfile.objects.all(), widget=forms.widgets.Select(attrs={'size': 1}))
    question = forms.ModelChoiceField(label='Вопрос', queryset=Question.objects.all(), widget=forms.widgets.Select(attrs={'size': 1}))
    admin = forms.ModelChoiceField(label='Администратор', queryset=UserProfile.objects.all(), widget=forms.widgets.Select(attrs={'size': 1}))

class CheckedAnswerForm(forms.ModelForm):
    answer = forms.ModelChoiceField(label='', queryset=CheckedAnswer.objects.all(), widget=forms.widgets.RadioSelect)
    class Meta:
        model = CheckedAnswer
        fields = ('answer',)

# class UserAnswerForm(forms.Form):
#     checked = 
#     class Meta:
#         model = CheckedAnswer
#         fields = ('text', 'checked', 'question')