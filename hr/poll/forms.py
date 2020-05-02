from django import forms
from .models import UserProfile, Question, Poll
  
  
class ProfileCreationForm(forms.ModelForm):  
  
    class Meta:  
        model = UserProfile  
        fields = ['age', 'type_user']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('text', 'type', 'image', 'time_limit', 'answers')

# class PollForm(forms.ModelForm):
#     class Meta:
#         model = Poll
#         fields = ('name', 'date_pub', 'user', 'time_limit', 'questions')


class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ('name', 'date_pub', 'user', 'time_limit', 'questions')
