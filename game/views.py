from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from game.models import Profile
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from django.http import JsonResponse
from django.http import HttpResponse
from game.forms import PersonalForm
import random
import logging

logger = logging.getLogger('django')

# def register(request):
#     if request.method == 'POST':
#         logger.debug("Form submitted via POST")
#         username = request.POST['username']
#         email = request.POST['email']
#         phone_number = request.POST['phone_number']
#         password = request.POST['password']
#         confirm_password = request.POST['confirm_password']

#         # Validate passwords
#         if password != confirm_password:
#             logger.error("Passwords do not match")
#             return render(request, 'register.html', {'error': 'Passwords do not match'})

#         # Create the user
#         try:
#             # Create the user
#             user = User.objects.create_user(username=username, email=email, password=password)
#             logger.debug(f"User {username} created successfully")
            
#             # Create the profile with the phone number
#             Profile.objects.create(user=user, phone_number=phone_number)
#             logger.debug(f"Profile for {username} created successfully")

#             # Automatically log the user in after registration
#             auth_login(request, user)
#             logger.debug(f"User {username} logged in successfully")

#             # Redirect to the homepage after successful registration
#             return redirect('homepage')

#         except Exception as e:
#             logger.error(f"Error creating user or profile: {e}")
#             return render(request, 'register.html', {'error': str(e)})

#     return render(request, 'register.html')

# @login_required
# def homepage(request):
#     user = request.user  # Get the logged-in user
#     profile = Profile.objects.get(user=user)  # Get the profile associated with the user
    
#     # Pass both user and profile data to the template
#     context = {
#         'username': user.username,
#         'email': user.email,
#         'phone_number': profile.phone_number,  # Assuming phone is stored in Profile model
#     }
#     return render(request, 'homepage.html', context)

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
    
    form = PersonalForm()
    
    # if request.method == "POST":
    #     form = PersonalForm(request.POST)
        
    #     if form.is_valid():
            
    #         name = form.cleaned_data['name']
    #         password = form.cleaned_data['password']
    #         confirm_password = form.cleaned_data['confirm_password']
    #         model=""
    #         model=Profile(name=name,password=password,confirm_password=confirm_password)
    #         model.save()
    
    if request.method == 'POST':
        logger.debug("Form submitted via POST")
        username = request.POST['username']
        # email = request.POST['email']
        # phone_number = request.POST['phone_number']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Validate passwords
        if password != confirm_password:
            logger.error("Passwords do not match")
            return render(request, 'register.html', {'error': 'Passwords do not match'})
        
        # Create the user
        try:
            # Create the user
            user = User.objects.create_user(username=username, password=password)
            logger.debug(f"User {username} created successfully")
            
            # # Create the profile
            # Profile.objects.create(user=user, password=password)
            # logger.debug(f"Profile for {username} created successfully")

            # Automatically log the user in after registration
            auth_login(request, user)
            logger.debug(f"User {username} logged in successfully")

            # Redirect to the homepage after successful registration
            return redirect('homepage')

        except Exception as e:
            logger.error(f"Error creating user or profile: {e}")
            return render(request, 'register.html', {'error': str(e)})

            
    # return HttpResponseRedirect("/login")
        
        # context = {'registerform':form}
    return render(request, 'game/register.html', {"form": form})

def login(request):
    return render(request, 'game/login.html')