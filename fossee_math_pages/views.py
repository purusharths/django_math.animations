from django.shortcuts import render
from .forms import UserLoginForm
from .models import (profile, User, )
from os import listdir, path, sep, makedirs, remove
from datetime import datetime, date
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect


def index(request):
    return render(request, "fossee_math_pages/index.html")

def internship(request):
    return render(request, "fossee_math_pages/internship.html")

def topics(request):
    return render(request, "fossee_math_pages/topics.html")

def is_superuser(user):
    return user.is_superuser


def dashboard(request):
    user = request.user
    role = profile.objects.get(user_id=user.id)
    if role.role == 'staff' or role.role == 'intern':
        return render(request, "fossee_math_pages/dashboard.html")
    else:
        return redirect('logout')


def user_login(request):
    user = request.user

    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data
            login(request, user)

            if is_superuser(user):
                return redirect('/admin')

            usr_type = profile.objects.get(user_id=user.id)
            if usr_type.role == 'intern' or usr_type.role == 'staff':
                return render(request, 'fossee_math_pages/dashboard.html')
            else:
                return render(request, 'fossee_math_pages/login.html', {"form": form})
        else:
            return render(request, 'fossee_math_pages/login.html', {"form": form})
    else:
        form = UserLoginForm()
        return render(request, "fossee_math_pages/login.html", {"form": form})


def user_logout(request):
    logout(request)
    return redirect('index')

# def InternForm(request):
#     if request.method == 'POST':
#         form = AddInternForm(request.POST)
#         if form.is_valid():
#             name = form.cleaned_data['name']
#             email = form.cleaned_data['email']
#             topic = form.cleaned_data['topic']

#     form = AddInternForm()
#     return render(request, 'fossee_math_pages/dashboard_admin.html', {'form': form})


def manage_intern(request):
    return render(request,'fossee_math_pages/manage_intern.html')

def aprove_contents(request):
    return render(request,'fossee_math_pages/aprove_contents.html')

def add_details(request):
    return render(request,'fossee_math_pages/intern_add_data.html')

def view_details(request):
    return render(request,'fossee_math_pages/intern_view_data.html')

def topic_details(request):
    return render(request,'fossee_math_pages/view_topic_details.html')

def add_intern(request):
    return render(request,'fossee_math_pages/add_intern.html')