from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
import random

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            # Create the user
            user = User.objects.create_user(username=username, email=email, password=password)
            # Create the user profile and save the phone number
            Profile.objects.create(user=user, phone=phone)

            auth_login(request, user)
            return redirect('profile')
        else:
            # Handle password mismatch
            return render(request, 'register.html', {'error': 'Passwords do not match'})
    return render(request, 'register.html')

@login_required
def homepage(request):
    user = request.user  # Get the logged-in user
    context = {
        'name': user.username,  # Pass the username to the template
    }
    return render(request, 'game/homepage.html', context)

# Generate an arithmetic question with no negative answers
def generate_question(request):
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    operation = random.choice(["+", "-"])

    if operation == "-":
        # Ensure the result is non-negative by making num1 >= num2
        if num1 < num2:
            num1, num2 = num2, num1

    question = f"{num1} {operation} {num2}"
    answer = eval(question)
    
    return JsonResponse({"question": question, "answer": answer})

# Validate the player's answer
def validate_answer(request):
    if request.method == 'POST':
        user_answer = int(request.POST.get('answer'))
        correct_answer = int(request.POST.get('correct_answer'))
        
        if user_answer == correct_answer:
            return JsonResponse({"result": "correct"})
        else:
            return JsonResponse({"result": "incorrect"})
        

def question_page(request):
    return render(request, 'game/game.html')

def game_select(request):
    return render(request, 'game/GameSelect.html')

def easy_mode(request):
    return render(request, 'game/easy.html')

def medium_mode(request):
    return render(request, 'game/medium.html')

def hard_mode(request):
    return render(request, 'game/hard.html')

def index(request):
    return render(request, 'game/index.html')


def homepage(request):
    return render(request, 'game/homepage.html')

def profile(request):
    return render(request, 'game/profile.html')

def register(request):
    return render(request, 'game/register.html')

def login(request):
    return render(request, 'game/login.html')