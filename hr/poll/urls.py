from django.urls import path, include

from .views import index, QuestionList, QuestionDetailsView, QuestionCreate, QuestionEdit, QuestionDelete, PollList, PollDetailsView, PollEdit, PollDelete, PollCreate

app_name = 'poll'
urlpatterns = [
    path('', PollList.as_view(), name='index'),
    path("details/<int:pk>", PollDetailsView.as_view(), name="poll_details"),
    path('create/', PollCreate.as_view(), name='poll_create'),
    path('edit/<int:pk>', PollEdit.as_view(), name='poll_edit'),
    path('delete/<int:pk>', PollDelete.as_view(), name='poll_delete'),
    path('questions/', QuestionList.as_view(), name='question_list'),
    path("questions/details/<int:pk>", QuestionDetailsView.as_view(), name="question_details"),
    path('question/create/', QuestionCreate.as_view(), name='question_create'),
    path('question/edit/<int:pk>', QuestionEdit.as_view(), name='question_edit'),
    path('question/delete/<int:pk>', QuestionDelete.as_view(), name='question_delete'),
]