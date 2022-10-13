from django.urls import path

from .views import index, add_question, add_option2, add_option, vote

urlpatterns = [
    path('', index, name="index"),
    path('add_question/', add_question, name="add_question"),
    path('add_option/', add_option2, name="add_option"),
    path('vote/<str:question_secondary_id>/', vote, name="vote")
]