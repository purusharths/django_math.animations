from django.shortcuts import render
from .forms import (UserLoginForm, )
from .models import (profile, User, )
from os import listdir, path, sep, makedirs, remove
from datetime import datetime, date
from django.contrib.auth import login
from django.shortcuts import render, redirect


def index(request):
    return render(request, "fossee_math_pages/index.html")


def pagenotfound(request):
    return render(request, "fossee_math_pages/404.html")


def internship(request):
    return render(request, "fossee_math_pages/internship.html")


def real_number_line(request):
    return render(request, "fossee_math_pages/real_number_line.html")


def realanalysis(request):
    return render(request, "fossee_math_pages/realanalysis.html")


def topics(request):
    return render(request, "fossee_math_pages/topics.html")


def is_superuser(user):
    return user.is_superuser

def dashboard_admin(request):
    return render(request,"fossee_math_pages/dashboard_admin.html")

def dashboard_intern(request):
    return render(request,"fossee_math_pages/dashboard_intern.html")


def login(request):
    try:
        # user = request.user
        # if is_superuser(user):
        #     return redirect('/admin')
        # if user.is_authenticated():
        #     if user.groups.filter(name='reviewer').count() > 0:
        #         return render(request, "../templates/login.html")
        #     return render(request, "../templates/login.html")

        if request.method == "POST":
            form = UserLoginForm(request.POST)
            # if form.is_valid():
            #     user = form.cleaned_data
            #     login(request, user)
            #     if user.groups.filter(name='reviewer').count() > 0:
            #         return render(request, "../templates/login.html")
            #     return render(request, "../templates/login.html")
            # else:
            #     return render(request, "../templates/login.html")
        else:
            return render(request, "../templates/fossee_math_pages/login.html")

    except:
        return render(request, "../templates/fossee_math_pages/login.html")
