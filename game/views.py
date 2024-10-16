import json
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, login
from game.models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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

# Generate an arithmetic question with no negative answers, adjusted based on mode
def generate_question(request, mode):
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)

    if mode == "easy":
        # Easy mode: only addition and subtraction
        operation = random.choice(["+", "-"])

        if operation == "-":
            # Ensure the result is non-negative by making num1 >= num2
            if num1 < num2:
                num1, num2 = num2, num1

        question = f"{num1} {operation} {num2}"
        answer = eval(question)
    
    elif mode == "medium":
        # Medium mode: addition, subtraction, and multiplication
        operation = random.choice(["+", "-", "*"])

        if operation == "-":
            # Ensure non-negative results
            if num1 < num2:
                num1, num2 = num2, num1

        question = f"{num1} {operation} {num2}"
        answer = eval(question)

    elif mode == "hard":
        # Hard mode: multiplication and division with larger numbers
        operation = random.choice(["*", "/"])

        if operation == "/":
            # Ensure the result is a whole number and avoid division by zero
            num2 = random.randint(1, 10)
            num1 = num2 * random.randint(1, 10)  # Ensure num1 is divisible by num2

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
        

def update_points(request):
    if request.method == 'POST':
        user = request.user

        # Try to get the profile or create it if it doesn't exist
        try:
            profile = user.profile  # This assumes OneToOneField is correctly set up
        except Profile.DoesNotExist:
            # Create the profile if missing
            profile = Profile.objects.create(user=user)

        # Get the points from the POST request
        data = json.loads(request.body)  # Read the JSON data
        new_points = int(data.get('points'))

        # Add the new points to the existing points
        profile.points += new_points
        profile.save()

        logger.debug(f"Points updated: {profile.points}")
        return JsonResponse({'status': 'success', 'points': profile.points})
    
    return JsonResponse({'status': 'error'}, status=400)

def question_page(request):
    return render(request, 'game/game.html')

def game_mode(request, mode):
    return render(request, 'game/game.html', {'mode': mode})

def index(request):
    return render(request, 'game/index.html')


@login_required
def homepage(request):
    user = request.user  # Get the logged-in user
    try:
        profile = user.profile  # This assumes OneToOneField is correctly set up
    except Profile.DoesNotExist:
        # Handle case where the profile doesn't exist
        profile = Profile.objects.create(user=user)  # Create a profile if missing

    return render(request, 'game/homepage.html', {
        'username': user.username,
        'points': profile.points
    })

@login_required
def profile(request):
    user = request.user  # Get the logged-in user
    try:
        profile = user.profile  # This assumes OneToOneField is correctly set up
    except Profile.DoesNotExist:
        # Handle case where the profile doesn't exist
        profile = Profile.objects.create(user=user)  # Create a profile if missing

    return render(request, 'game/profile.html', {
        'username': user.username,
        'points': profile.points
    })

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
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Validate passwords
        if password != confirm_password:
            # If passwords do not match, pass a flag to the template
            return render(request, 'game/register.html', {
                'form': form,
                'password_mismatch': True
            })
        
        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            return render(request, 'game/register.html', {
                'form': form,
                'username_taken': True  # Pass flag to display an error message in template
            })
        
        # Create the user
        try:
            # Create the user
            user = User.objects.create_user(username=username, password=password)
            # logger.debug(f"User {username} created successfully")

            # Create the corresponding profile for the user
            Profile.objects.create(username=username, password=password, confirm_password=confirm_password, points=0)
            
            # Automatically log the user in after registration
            auth_login(request, user)
            
            # # Create the profile
            # Profile.objects.create(user=user, password=password)
            # logger.debug(f"Profile for {username} created successfully")

            # # Automatically log the user in after registration
            # auth_login(request, user)
            # logger.debug(f"User {username} logged in successfully")
            
            # Pass a success message to the template to trigger the alert
            return render(request, 'game/register.html', {
                'form': form,
                'success': True,  # This will be used in JavaScript for triggering the alert
                'username': username
            })

            # # Redirect to login page after successful registration
            # return redirect('login')

        except Exception as e:
            logger.error(f"Error creating user or profile: {e}")
            return render(request, 'register.html', {'error': str(e)})

            
    # return HttpResponseRedirect("/login")
        
        # context = {'registerform':form}
    return render(request, 'game/register.html', {"form": form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Check if the username exists in the database
        try:
            user_exists = User.objects.get(username=username)
        except User.DoesNotExist:
            # If the username does not exist, show an error message
            return render(request, 'game/login.html', {
                'username_not_found': True  # This will trigger an error message in the template
            })
        

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # If the user is authenticated, log them in and redirect to homepage
            login(request, user)
            return redirect('homepage')
        else:
            # If login is unsuccessful, reload the login page and display error
            return render(request, 'game/login.html', {
                'login_failed': True  # This will be used for the alert in the template
            })

    return render(request, 'game/login.html')