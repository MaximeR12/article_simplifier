import ollama
import os

from django import template

from .forms import TextAnalysisForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .utils import analysis

from dotenv import load_dotenv
load_dotenv()


def homepage(request):
    print ("user:",request.user)
    context={"user" : request.user}
    return render(request, 'homepage.html', context)

def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username = username, password = password)
            login(request, user)
            messages.success(request, "Account created, you're now logged in")
            return redirect('homepage')
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {
        "form" : form,
        })

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You're now logged in")
            return redirect('homepage')
        else:
            messages.success(request, "Could not log you in, verify your username/password")
            return redirect('login')
    else:
        return render(request, 'login.html') 

def logout_user(request):
    logout(request)
    messages.success(request, "Succesfully Logged out !")
    return redirect('homepage')

def text_analysis_old(request):
    if request.user is None:
        messages.success(request, "You must be logged in to use the text Analysis")
        return redirect('login')
    else:
        if request.method == 'POST':
            input_text = request.POST["input_text"]
            output_language = request.POST["output_language"]
            output = analysis(input_text= input_text, output_language=output_language)
            return render(request, "analysis.html", {"output" : output, "prediction_done": True})
        else:
            return render(request, "analysis.html", {"prediction_done": False})

def text_analysis(request):
    if request.user is None:
        messages.success(request, "You must be logged in to use the text Analysis")
        return redirect('login')
    else:
        if request.method == 'POST':
            form = TextAnalysisForm(request.POST)
            if form.is_valid():
                input_text = form.cleaned_data['input_text']
                output_language = form.cleaned_data['output_language']
                output = analysis(input_text=input_text, output_language=output_language)
                return render(request, "analysis.html", {"output": output, "form": form, "prediction_done": True})
        else:
            form = TextAnalysisForm()
            return render(request, "analysis.html", {"form": form, "prediction_done": False})
