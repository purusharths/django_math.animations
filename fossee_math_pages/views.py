import random
from datetime import datetime

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.checks import messages
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from .forms import AddUserForm
from .forms import (UserLoginForm, add_data, )
from .models import ( data, AddUser)

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth.models import User
from django.contrib import messages, auth
import random
from .forms import AddUserForm, DeleteUserForm
from django.core.mail import send_mail
from django.conf import settings


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
    if request.user:
        intern_count = 0
        
        intern_count = AddUser.objects.filter(role='INTERN').count()
        staff_count = AddUser.objects.filter(role='STAFF').count()

        status_active = AddUser.objects.filter(status='ACTIVE').count()
        status_inactive = AddUser.objects.filter(status='INACTIVE').count()
        status_suspended = AddUser.objects.filter(status='SUSPENDED').count()
        date_joined = AddUser.objects.order_by('-date_joined')
        context = {

            'intern_count' : intern_count,
            'staff_count' : staff_count,
            'status_active' :status_active,
            'status_inactive' : status_inactive,
            'status_suspended' : status_suspended,
            'date_joined' : date_joined
        }
        return render(request, "fossee_math_pages/dashboard.html", context)
    else:

        return redirect('logout')


def user_login(request):
    user = request.user
    if is_superuser(user):
        return redirect('/admin')

    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data
            login(request, user)
            intern_count = 0
            intern_count = AddUser.objects.filter(role='INTERN').count()
            staff_count = AddUser.objects.filter(role='STAFF').count()

            status_active = AddUser.objects.filter(status='ACTIVE').count()
            status_inactive = AddUser.objects.filter(role='INACTIVE').count()
            status_suspended = AddUser.objects.filter(role='SUSPENDED').count()
            context = {
                'intern_count': intern_count,
                'staff_count': staff_count,
                'status_active': status_active,
                'status_inactive': status_inactive,
                'status_suspended': status_suspended
            }
            return render(request, "fossee_math_pages/dashboard.html", context)
        else:
            return render(request, "fossee_math_pages/login.html", {"form": form})
    else:
        form = UserLoginForm()
        return render(request, "fossee_math_pages/login.html", {"form": form})


def user_logout(request):
    logout(request)
    return redirect('index')


@login_required
def add_user(request):
    temp = AddUserForm()
    if request.method == 'POST':
        # register user
        name = request.POST['name']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        topic = request.POST['topic']
        phone = request.POST['phone']
        role = request.POST['role']
        if User.objects.filter(email=email).exists():
            messages.error(request, 'That email is being used')
            return redirect('add_user')
        else:
            try:
                password = random.randint(0, 99999999)
                passwordstr = str(password)
                user = User.objects.create_user(username=name, email=email, password=password, first_name=firstname, last_name=lastname)
                u_id = User.objects.get(username=name)
                if role=='INTERN':
                    addusr = AddUser(user_id=u_id.id, name=name, email=email, topic=topic, phone=phone, role=role,
                                temp_password=password)
                    addusr.save()
                else:
                    addusr = AddUser(user_id=u_id.id, name=name, email=email, topic=topic, phone=phone, role=role,
                                    temp_password=password,status='ACTIVE')
                    addusr.save()

                send_mail(
                    'FOSSEE ANIMATION MATH',
                    'Thank you for registering with fossee_math. Your password is ' + passwordstr,
                    'fossee_math',
                    [email, 'fossee_math@gmail.com'],
                    fail_silently=True, )
            except:
                usr = User.objects.get(username=name)
                usr.delete()
                messages.error(request, 'Some error occured !')
                return redirect('add_user')
            messages.success(request, 'User Added!')
            return redirect('add_user')

    return render(request, 'fossee_math_pages/add_user.html', {'form': temp})


def manage_intern(request):
    users = User.objects.all()
    details = AddUser.objects.all()
    context = {
        'users': users,
        'details': details
    }
    if request.method == 'POST':
        # register user
        u_id = request.POST['id']
        option = request.POST['option_select']
        AddUser.objects.filter(user_id=u_id).update(status=option)

    return render(request, 'fossee_math_pages/manage_intern.html', context)


def aprove_contents(request):
    return render(request, 'fossee_math_pages/aprove_contents.html')


@login_required
def add_details(request):
    form = add_data
    if request.method == 'POST':
        form = add_data(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user.id
            post.save()
            form = add_data
            return render(request, 'fossee_math_pages/intern_add_data.html', {'form': form})
    return render(request, 'fossee_math_pages/intern_add_data.html', {'form': form})


@login_required
def view_details(request):
    try:
        usr=request.user
        details=AddUser.objects.get(user_id=usr.id)
        resources = data.objects.filter(user=request.user.id)
        context = {
            'resources': resources,
            'usr':details,
        }
        return render(request, 'fossee_math_pages/intern_view_topic.html', context)
    except:
        return render(request, 'fossee_math_pages/intern_view_topic.html')


@login_required
def edit_details(request):
    try:
        resources = data.objects.filter(user=request.user.id)
        res = ""
        form = ""
        if request.POST:
            if request.POST['option'] is not None:
                data_id = request.POST['option']
                res = data.objects.get(id=data_id)
                resource = data.objects.get(id=res.id)
                print(resource)
                form = add_data(instance=resource)

        if request.POST:
            if request.POST['data_edit']:
                print("save")
                # form.save()

        context = {
            'resources': resources,
            'modify': res,
            'form_edit': form,
        }

        return render(request, 'fossee_math_pages/intern_edit_data.html', context)
    except:
        return render(request, 'fossee_math_pages/intern_edit_data.html')


def topic_details(request):
    return render(request, 'fossee_math_pages/view_topic_details.html')


class AddUserView(AddUser):
    def create_user(self, request, *args, **kwargs):
        name = self.name
        email = self.email
        password = random.randint(0, 99999999)
        user = User.objects.create_user(name, email, password)
        user.save(using=self._db)
        return user
