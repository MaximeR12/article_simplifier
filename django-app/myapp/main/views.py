import os
import logging
from django import template
from django.urls import reverse
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from asgiref.sync import sync_to_async
from .forms import TextAnalysisForm
from .utils import llm_api_call
from .models import Analysis

from dotenv import load_dotenv
load_dotenv()


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

logger = logging.getLogger(__name__)

def homepage(request):
    return render(request, 'homepage.html')

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "You're now logged in")
            return redirect('homepage')
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out")
    return redirect('homepage')

def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created, you're now logged in")
            return redirect('homepage')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def user_profile(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.save()
        messages.success(request, "Profile updated successfully")
        return redirect('user_profile')
    return render(request, 'profile.html', {'user': request.user})

@login_required
def analysis(request):
    if request.method == 'POST':
        form = TextAnalysisForm(request.POST)
        if form.is_valid():
            input_text = form.cleaned_data['input_text']
            output_language = form.cleaned_data['output_language']
            logger.info(f"User {request.user.username} submitted text for analysis in {output_language}")
            try:
                result = llm_api_call(input_text, output_language)
                analysis = Analysis.objects.create(
                    user=request.user,
                    input_text=input_text,
                    output_text=result,
                    output_language=output_language
                )
                logger.info(f"Analysis created for user {request.user.username}, ID: {analysis.id}")
                return render(request, 'result.html', {'analysis': analysis})
            except Exception as e:
                logger.error(f"Error during analysis for user {request.user.username}: {str(e)}")
                messages.error(request, "An error occurred during analysis. Please try again.")
                return redirect('analysis')
    else:
        form = TextAnalysisForm()
    return render(request, 'analysis.html', {'form': form})
