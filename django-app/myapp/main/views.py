import os
import logging
from django import template
from django.urls import reverse
from .forms import TextAnalysisForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .utils import analysis

from dotenv import load_dotenv
load_dotenv()


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Analysis  # Add this import

def homepage(request):
    items = Analysis.objects.all().order_by('-timestamp')
    paginator = Paginator(items, 10)  # Show 10 items per page
    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    context = {"user": request.user, "items": items}
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
            return redirect(reverse('homepage'))
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {
        "form" : form,
        })

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

@login_required
def text_analysis(request):
    if request.method == 'POST':
        form = TextAnalysisForm(request.POST)
        if form.is_valid():
            input_text = form.cleaned_data['input_text']
            output_language = form.cleaned_data['output_language']
            try:
                output = analysis(input_text=input_text, output_language=output_language)
                # Save the analysis
                Analysis.objects.create(
                    user=request.user,
                    input_text=input_text,
                    output_text=output,
                    output_language=output_language
                )
                return render(request, "analysis.html", {"output": output, "form": form, "prediction_done": True})
            except Exception as e:
                print(f"An error occurred during analysis: {str(e)}")
                messages.error(request, f"An error occurred during analysis: {str(e)}")
                logging.error(f"An error occurred during analysis: {str(e)}")
                return render(request, "analysis.html", {"form": form, "prediction_done": False})
    form = TextAnalysisForm()
    return render(request, "analysis.html", {"form": form, "prediction_done": False})

@login_required
def user_profile(request):
    if request.method == 'POST':
        # Handle form submission to update user profile
        # You can add fields like email, first name, last name, etc.
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.save()
        messages.success(request, "Profile updated successfully")
        return redirect('user_profile')
    return render(request, 'profile.html', {'user': request.user})
