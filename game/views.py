from django.shortcuts import render

from django.http import JsonResponse
import random

# Generate an arithmetic question
def generate_question(request):
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    operation = random.choice(["+", "-"])
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