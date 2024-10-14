from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # The main game page
    path('generate_question/<str:mode>/', views.generate_question, name='generate_question'),  # API to generate questions
    path('validate_answer/', views.validate_answer, name='validate_answer'),  # API to validate answers
    path('update-points/', views.update_points, name='update_points'),
    path('question/', views.question_page, name='question_page'), 
    path('profile/', views.profile, name='profile'),
    path('homepage/', views.homepage, name='homepage'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('<str:mode>/', views.game_mode, name='game_mode'),  # Handle game modes (easy, medium, hard)
]