from django.urls import path
from . import views

urlpatterns = [
    path('', views.question_page, name='question_page'),  # The main game page
    path('generate_question/', views.generate_question, name='generate_question'),  # API to generate questions
    path('validate_answer/', views.validate_answer, name='validate_answer'),  # API to validate answers
    path('gameselect/', views.game_select, name='game_select'),
]
