from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.timezone import now

from .forms import (UserLoginForm, add_data, AddForm, )
from .models import (profile, data, )


def index(request):
    return render(request, "fossee_math_pages/index.html")


def internship(request):
    return render(request, "fossee_math_pages/internship.html")


def topics(request):
    return render(request, "fossee_math_pages/topics.html")


def is_superuser(user):
    return user.is_superuser


@login_required
def dashboard(request):
    user = request.user
    role = profile.objects.get(user_id=user.id)
    if role.role == 'staff' or role.role == 'intern':
        # InternForm()
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


def add_intern(request):
    if request.method == 'POST':
        form = AddForm(request.POST)
    form = AddForm()
    return render(request, 'fossee_math_pages/add_intern.html', {'form': form})


def manage_intern(request):
    return render(request, 'fossee_math_pages/manage_intern.html')


def aprove_contents(request):
    return render(request, 'fossee_math_pages/aprove_contents.html')


@login_required
def add_details(request):
    form = add_data
    if request.method == 'POST':
        form = add_data(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user_id = request.user.id
            post.post_date = now()
            post.save()
            form = add_data
            return render(request, 'fossee_math_pages/intern_add_data.html', {'form': form})
    return render(request, 'fossee_math_pages/intern_add_data.html', {'form': form})


@login_required
def view_details(request):
    try:
        resources = data.objects.filter(user_id=request.user.id)
        return render(request, 'fossee_math_pages/intern_view_data.html', {'resources': resources})
    except:
        return render(request, 'fossee_math_pages/intern_view_data.html')


@login_required
def edit_details(request):
    try:
        resources = data.objects.filter(user_id=request.user.id)
        return render(request, 'fossee_math_pages/intern_edit_data.html', {'resources': resources})
    except:
        return render(request, 'fossee_math_pages/intern_edit_data.html')


def add_intern(request):
    return render(request, 'fossee_math_pages/add_intern.html')


def topic_details(request):
    return render(request, 'fossee_math_pages/view_topic_details.html')
