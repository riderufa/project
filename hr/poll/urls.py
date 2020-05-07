from django.urls import path, include

from .views import index
from .view_question import QuestionCreate, QuestionDetail, QuestionEdit, QuestionDelete, QuestionList
from .view_poll import PollList, PollCreate, PollEdit, PollDelete, PollDetail, PollSet
from .view_answer import AnswerDelete, AnswerEdit, AnswerList, AnswerCreate
from .view_kit import KitList, KitCreate, KitDelete, KitEdit
from .view_user import question_get_answer, user_question_list, add_answers

app_name = 'poll'
urlpatterns = [
    path('', PollList.as_view(), name='index'),
    path("details/<int:pk>", PollDetail.as_view(), name="poll_details"),
    path('create/', PollCreate.as_view(), name='poll_create'),
    path('edit/<int:pk>', PollEdit.as_view(), name='poll_edit'),
    path('delete/<int:pk>', PollDelete.as_view(), name='poll_delete'),
    path('set/<int:pk>', PollSet.as_view(), name='poll_set'),
    path("kit/list/<int:pk>", KitList.as_view(), name="kit_list"),
    path('kit/create/<int:pk>', KitCreate.as_view(), name='kit_create'),
    path('kit/edit/<int:pk>', KitEdit.as_view(), name='kit_edit'),
    path('kit/delete/<int:pk>', KitDelete.as_view(), name='kit_delete'),
    path('user/get_answer/<int:pk>', question_get_answer, name='question_get_answer'),
    # path('user/save_answer/<int:pk>', question_save_answer, name='question_save_answer'),
    path("user/questions/<int:pk>", user_question_list, name="user_question_list"),
    path('questions/', QuestionList.as_view(), name='question_list'),
    path("questions/details/<int:pk>", QuestionDetail.as_view(), name="question_details"),
    path('question/create/', QuestionCreate.as_view(), name='question_create'),
    path('question/edit/<int:pk>', QuestionEdit.as_view(), name='question_edit'),
    path('question/delete/<int:pk>', QuestionDelete.as_view(), name='question_delete'),
    path("answer/list/<int:pk>", AnswerList.as_view(), name="answer_list"),
    path('answer/edit/<int:pk>', AnswerEdit.as_view(), name='answer_edit'),
    path('answer/create/<int:pk>', AnswerCreate.as_view(), name='answer_create'),
    path('answer/delete/<int:pk>', AnswerDelete.as_view(), name='answer_delete'),
    path('user/get_answer/add/', add_answers, name='add_answers'),
]