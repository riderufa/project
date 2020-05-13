from django.urls import path, include

from .views import index
from .view_question import QuestionCreate, QuestionDetail, QuestionEdit, QuestionDelete, QuestionList
from .view_poll import PollList, PollCreate, PollEdit, PollDelete, PollDetail, PollSet
from .view_answer import AnswerDelete, AnswerEdit, AnswerList, AnswerCreate
from .view_kit import KitList, KitCreate, KitDelete, KitEdit
from .view_user import question_get_answer, check_poll, add_answers
from .view_checked_poll import UserCheckedPollList, AdminCheckedPollList
from .view_stat import get_stat
from .view_admin import UserList, QuestionUserList, QuestionPollList, PollUserList, PollQuestionList, UserPollList, UserQuestionList

app_name = 'poll'
urlpatterns = [
    path('', PollList.as_view(), name='index'), # Список опросов
    path("details/<int:pk>", PollDetail.as_view(), name="poll_details"), # Опрос подробно
    path('create/', PollCreate.as_view(), name='poll_create'), # Создать опрос
    path('edit/<int:pk>', PollEdit.as_view(), name='poll_edit'), # Редактировать опрос
    path('delete/<int:pk>', PollDelete.as_view(), name='poll_delete'), # Удалить опрос
    path('set/<int:pk>', PollSet.as_view(), name='poll_set'), # Присвоить опрос пользователю
    path("kit/list/<int:pk>", KitList.as_view(), name="kit_list"), # Список элементов связующей таблицы (балл вопроса в опросе)
    path('kit/create/<int:pk>', KitCreate.as_view(), name='kit_create'), # Создать элемент связующей таблицы (балл вопроса в опросе)
    path('kit/edit/<int:pk>', KitEdit.as_view(), name='kit_edit'), # Редактировать элемент связующей таблицы (балл вопроса в опросе)
    path('kit/delete/<int:pk>', KitDelete.as_view(), name='kit_delete'), # Удалить элемент связующей таблицы (балл вопроса в опросе)
    path('user/get_answer/<int:pk>', question_get_answer, name='question_get_answer'), # Список ответов в вопросе пользователя
    path("check/poll/<int:pk>", check_poll, name="check_poll"), # Список вопросов в опросе пользователя
    path('questions/', QuestionList.as_view(), name='question_list'), # Список вопросов
    path("questions/details/<int:pk>", QuestionDetail.as_view(), name="question_details"), # Вопрос подробно
    path('question/create/', QuestionCreate.as_view(), name='question_create'), # Создать вопрос
    path('question/edit/<int:pk>', QuestionEdit.as_view(), name='question_edit'), # Редактировать вопрос
    path('question/delete/<int:pk>', QuestionDelete.as_view(), name='question_delete'), # Удалить вопрос
    path("answer/list/<int:pk>", AnswerList.as_view(), name="answer_list"), # Список ответов
    path('answer/edit/<int:pk>', AnswerEdit.as_view(), name='answer_edit'), # Редактировать ответ
    path('answer/create/<int:pk>', AnswerCreate.as_view(), name='answer_create'), # Создать ответ
    path('answer/delete/<int:pk>', AnswerDelete.as_view(), name='answer_delete'), # Удалить ответ
    path('user/get_answer/add/', add_answers, name='add_answers'), # Сохранение ответов на вопрос пользователя в базе
    path('user_checked_poll/list', UserCheckedPollList.as_view(), name='user_checked_poll_list'), # Список пройденных опросов пользователя
    path('admin_checked_poll/list', AdminCheckedPollList.as_view(), name='admin_checked_poll_list'), # Список всех пройденных опросов
    path('stat/', get_stat, name='get_stat'), # Валидация опроса и сбор статистики
    path("user/list/", UserList.as_view(), name="user_list"), # Список пользователей
    path("question/user/list/<int:pk>", QuestionUserList.as_view(), name="question_user_list"), # Список пользователей вопроса
    path("question/poll/list/<int:pk>", QuestionPollList.as_view(), name="question_poll_list"), # Список опросов вопроса
    path("poll/user/list/<int:pk>", PollUserList.as_view(), name="poll_user_list"), # Список пользователей опроса
    path("poll/question/list/<int:pk>", PollQuestionList.as_view(), name="poll_question_list"), # Список вопросов опроса
    path("user/poll/list/<int:pk>", UserPollList.as_view(), name="user_poll_list"), # Список опросов пльзователя
    path("user/question/list/<int:pk>", UserQuestionList.as_view(), name="user_question_list"), # Список вопросов пользователя
]