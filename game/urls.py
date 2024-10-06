from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # The main game page
    path('generate_question/', views.generate_question, name='generate_question'),  # API to generate questions
    path('validate_answer/', views.validate_answer, name='validate_answer'),  # API to validate answers
    path('gameselect/', views.game_select, name='game_select'),
    path('question/', views.question_page, name='question_page'), 
    path('easy/', views.easy_mode, name='easy_mode'),
    path('medium/', views.medium_mode, name='medium_mode'),
    path('hard/', views.hard_mode, name='hard_mode'),
    path('profile/', views.profile, name='profile'),
    path('homepage/', views.homepage, name='homepage'),
    path('index/', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
]
