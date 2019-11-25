from django.shortcuts import render
from .forms import (UserLoginForm,)
from .models import (profile, User,)
from os import listdir, path, sep, makedirs, remove
from datetime import datetime, date
from django.contrib.auth import login
from django.shortcuts import render, redirect

def index(request):
    return render(request, "../templates/index.html")

def is_superuser(user):
    return user.is_superuser

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
            return render(request,"../templates/login.html")

    except:
        return render(request, "../templates/login.html")