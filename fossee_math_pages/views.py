import random
import re

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from email_validator import validate_email, EmailNotValidError

from .forms import (AddUserForm1, AddUserForm2, UserLoginForm, AddInternship, ManageInternship, AddIntern, add_topic,
                    ManageIntern, add_subtopic, AssignTopic, data, AproveContents, EditMedia)
from .models import (UserDetails, Internship, Intern, Topic, Subtopic, AssignedTopics, Data)


#  pic = request.FILES
#         internship_thumbnail = pic['internship_thumbnail']
@login_required
def admin_add_internship(request):
    form = AddInternship()
    if request.method == 'POST':
        internship_topic = request.POST['internship_topic']
        form = AddInternship(request.POST, request.FILES)
        print(form)
        if Internship.objects.filter(internship_topic=internship_topic).exists():
            messages.error(request, 'That internship already exist')
            return redirect('admin_add_internship')
        if form.is_valid():
            form.save()
            messages.success(request, 'Internship added')
            return redirect('admin_add_internship')
        else:
            messages.error(request, 'Some error occured')
            return redirect('admin_add_internship')
    form = AddInternship()
    context = {
        'form': form,
    }
    return render(request, 'fossee_math_pages/admin_add_internship.html', context)


@login_required
def admin_add_user(request):
    form = AddUserForm1()
    sub_form = AddUserForm2()
    if request.method == 'POST':
        # register user
        firstname = request.POST['first_name']
        lastname = request.POST['last_name']
        username = firstname + " " + lastname
        email = request.POST['email']
        user_role = request.POST['user_role']
        user_phone = request.POST['user_phone']
        user_status_inactive = 'INACTIVE'
        user_status_active = 'ACTIVE'

        regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'That email is being used')
            return redirect('admin_add_user')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'That username is being used')
            return redirect('admin_add_user')
        if firstname.isdigit():
            messages.error(request, 'Firstname cannot have numbers')
            return redirect('admin_add_user')
        if regex.search(firstname):
            messages.error(request, 'Firstname cannot have special characters')
            return redirect('admin_add_user')
        if lastname.isdigit():
            messages.error(request, 'Lastname cannot have numbers')
            return redirect('admin_add_user')
        if regex.search(lastname):
            messages.error(request, 'Lastname cannot have special characters')
            return redirect('admin_add_user')
        try:
            v = validate_email(email)
            val_email = v["email"]
        except EmailNotValidError as e:
            messages.error(request, 'Invalid Email ID')
            return redirect('admin_add_user')

        try:
            password = random.randint(0, 99999999)
            passwordstr = str(password)
            user = User.objects.create_user(username=username, email=email, password=password, first_name=firstname,
                                            last_name=lastname)
            u_id = User.objects.get(username=username)

            if user_role == 'INTERN':
                addusr = UserDetails(user_id=u_id, user_phone=user_phone, user_role=user_role,
                                     user_temp_password=password, user_status=user_status_inactive)
                addusr.save()
            if user_role == 'STAFF':
                user.is_staff = True
                user.save()
                addusr = UserDetails(user_id=u_id, user_phone=user_phone, user_role=user_role,
                                     user_temp_password=password, user_status=user_status_active)
                addusr.save()

            send_mail(
                'FOSSEE ANIMATION MATH',
                'Thank you for registering with fossee_math. Your password is ' + passwordstr,
                'fossee_math',
                [email, 'fossee_math@gmail.com'],
                fail_silently=True, )
        except:
            usr = User.objects.get(username=email)
            usr.delete()
            messages.error(request, 'Some error occured !')
            return redirect('admin_add_user')
        messages.success(request, 'User Added!')
        return redirect('admin_add_user')
    context = {
        'form': form,
        'sub_form': sub_form,
    }
    return render(request, 'fossee_math_pages/admin_add_user.html', context)


@login_required
def admin_manage_internship(request):
    manage_internships = Internship.objects.order_by('-internship_start_date')
    form = ManageInternship
    if request.method == 'POST':
        int_id = request.POST["id"]
        obj = get_object_or_404(Internship, id=int_id)
        form = ManageInternship(request.POST or None, instance=obj)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            messages.success(request, "Changed")
            return redirect('admin_manage_internship')
        else:
            messages.error(request, "Error")
            return redirect('admin_manage_internship')
    context = {
        'manage_internships': manage_internships,
        'form': form
    }
    return render(request, 'fossee_math_pages/admin_manage_internship.html', context)


@login_required
def admin_add_intern(request):
    user = User.objects.all()
    interns = Intern.objects.all()
    form = AddIntern(user)
    internships = Internship.objects.all()
    if request.method == 'POST':
        intern_name = request.POST['user_id']
        topic = request.POST['internship_id']
        usr = UserDetails.objects.get(id=intern_name)
        print(usr)
        print("\n------------", intern_name, "-------------\n")
        temp1 = User.objects.get(username=usr)
        print("\n------------", temp1, "-------------\n")
        temp2 = Internship.objects.get(id=topic)
        if Intern.objects.filter(user_id=temp1).exists():
            messages.error(request, 'That intern has an internship')
            return redirect('admin_add_intern')
        data = Intern(user_id=temp1, internship_id=temp2)
        data.save()
        messages.success(request, 'Intern added with internship')
        return redirect('admin_add_intern')

    context = {
        'internships': internships,
        'form': form,
        'interns': interns,
    }
    return render(request, 'fossee_math_pages/admin_add_intern.html', context)


@login_required
def admin_view_intern(request, id):
    datas = Intern.objects.filter(internship_id=id)
    form = ManageIntern
    if request.method == 'POST':
        int_id = request.POST["id"]
        obj = get_object_or_404(UserDetails, id=int_id)
        form = ManageIntern(request.POST or None, instance=obj)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            messages.success(request, "Changed")
            return redirect('admin_view_intern')
        else:
            messages.error(request, "Error")
            return redirect('admin_view_intern')

    context = {
        'datas': datas,
        'form': form,
    }
    return render(request, 'fossee_math_pages/admin_view_intern.html', context)


@login_required
def admin_view_intership(request):
    internship = Internship.objects.all()
    topic = Topic.objects.all()
    subtopic = Subtopic.objects.all()

    context = {
        'internship': internship,
        'topics': topic,
        'subtopic': subtopic,
    }

    return render(request, 'fossee_math_pages/admin_view_internship.html', context)


@login_required
def admin_manage_intern(request):
    datas = UserDetails.objects.filter(user_role="INTERN")
    form = ManageIntern
    if request.method == 'POST':
        int_id = request.POST["id"]
        obj = get_object_or_404(UserDetails, id=int_id)
        form = ManageIntern(request.POST or None, instance=obj)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            messages.success(request, "Changed")
            return redirect('admin_manage_intern')
        else:
            messages.error(request, "Error")
            return redirect('admin_manage_intern')

    context = {
        'datas': datas,
        'form': form,
    }
    return render(request, 'fossee_math_pages/admin_manage_intern.html', context)


@login_required
def admin_view_users(request):
    datas = UserDetails.objects.all()
    user_contains_query = request.GET.get('title_contains')
    if user_contains_query != '' and user_contains_query is not None:
        datas = UserDetails.objects.filter(user_id__username__contains=user_contains_query)
    if user_contains_query == "STAFF" or user_contains_query == "staff":
        datas = UserDetails.objects.filter(user_role="STAFF")
    if user_contains_query == "INTERN" or user_contains_query == "intern":
        datas = UserDetails.objects.filter(user_role="INTERN")

    paginator = Paginator(datas, 5)  # Show 25 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'datas': page_obj,
    }
    return render(request, 'fossee_math_pages/admin_view_users.html', context)


@login_required
def dashboard(request):
    return render(request, 'fossee_math_pages/dashboard.html')


def home_view_data(request, id):
    details = Internship.objects.get(id=id)
    topics = Topic.objects.filter(internship_id_id=id)
    subtopics = Subtopic.objects.all()
    context = {
        'details': details,
        'topics': topics,
        'subtopics': subtopics,
    }
    return render(request, 'fossee_math_pages/home_view_data.html', context)


def home_details(request, id):
    subtopic = Subtopic.objects.get(id=id)
    ver = ""
    try:
        data = Data.objects.all()
    except Data.DoesNotExist:
        data = None

    context = {
        'subtopic': subtopic,
        'datas': data,
        'ver': ver,
    }
    return render(request, 'fossee_math_pages/home_details.html', context)


def index(request):
    datas = ""
    datass = ""
    page_obj = ""
    search_contains_query = request.GET.get('title_contains')

    interships = Internship.objects.filter(internship_status='COMPLETED')

    if search_contains_query != '' and search_contains_query is not None:
        datas = Subtopic.objects.filter(subtopic_name__icontains=search_contains_query)
        datass = Subtopic.objects.filter(topic_id__topic_name__contains=search_contains_query)

    if datas:
        paginator = Paginator(datas, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

    if datass:
        paginator = Paginator(datass, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

    context = {
        'datas': page_obj,
        'internship': interships,
    }

    return render(request, 'fossee_math_pages/index.html', context)


@login_required
def intern_add_data(request, t_id):
    user = request.user
    e_data = Data.objects.filter(subtopic_id=t_id)
    subtopic = Subtopic.objects.get(id=t_id)
    form = data()

    if request.method == 'POST':
        content = request.POST.get('data_content')
        img = request.FILES.get('image')
        video = request.FILES.get('video')
        status = "WAITING"

        if content == "" or content == " ":
            content = "NULL"

        if img == "" or img == " ":
            img = "NULL"

        if video == "" or video == " ":
            video = "NULL"

        add_data = Data(data_content=content, data_status=status, data_image=img,
                        data_video=video, subtopic_id_id=t_id,
                        user_id_id=user.id)
        add_data.save()

    context = {
        'topic': e_data,
        'form': form,
        'subtopic': subtopic,
    }
    return render(request, 'fossee_math_pages/intern_add_data.html', context)


@login_required
def intern_update_data(request, id):
    instance = Data.objects.get(id=id)
    subtopic = Subtopic.objects.get(id=instance.subtopic_id.pk)
    t_id = instance.subtopic_id.pk
    form = data(request.POST or None, instance=instance)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        return redirect('intern_add_data', t_id)

    context = {
        'form': form,
        'subtopic': subtopic,
    }

    return render(request, 'fossee_math_pages/intern_update_data.html', context)


@login_required
def intern_update_media(request, id):
    instance = Data.objects.get(id=id)
    subtopic = Subtopic.objects.get(id=instance.subtopic_id.pk)
    t_id = instance.subtopic_id.pk
    form = EditMedia(request.POST or None, instance=instance)
    if request.POST:
        if form.is_valid():
            img = request.FILES.get('data_image')
            video = request.FILES.get('data_video')
            instance = Data.objects.get(id=id)
            instance.data_image = img
            instance.data_video = video
            instance.save()
            return redirect('intern_add_data', t_id)

    context = {
        'form': form,
        'subtopic': subtopic,
    }

    return render(request, 'fossee_math_pages/intern_update_media.html', context)


@login_required
def intern_delete_data(request, id):
    instance = Data.objects.get(id=id)
    t_id = instance.subtopic_id.pk
    instance.delete()
    return redirect('intern_add_data', t_id)


@login_required
def intern_view_internship(request):
    # internship = Internship.objects.filter(internship_status='ACTIVE')
    internship = AssignedTopics.objects.get(user_id_id=request.user.id)
    topics = Topic.objects.all()
    subtopics = Subtopic.objects.all()

    context = {
        'internship': internship,
        'topics': topics,
        'subtopics': subtopics,
    }
    return render(request, 'fossee_math_pages/intern_view_internship.html', context)


@login_required
def intern_view_topic(request):
    assigned_topic = AssignedTopics.objects.get(user_id=request.user.id)
    subtopic = Subtopic.objects.filter(topic_id=assigned_topic.topic_id)

    context = {
        'assigned': assigned_topic,
        'subtopic': subtopic,
    }
    return render(request, 'fossee_math_pages/intern_view_topic.html', context)


def internship(request):
    return render(request, 'fossee_math_pages/internship.html')


def user_login(request):
    user = None
    user = request.user

    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            try:
                user = form.authenticate_user()
                login(request, user)
                if request.user.is_staff:
                    return redirect(dashboard)
                else:
                    internship = Intern.objects.get(user_id=request.user.pk)
                    internship_ststus = Internship.objects.get(id=internship.internship_id_id)
                    if internship_ststus.internship_status == 'COMPLETED':
                        form = UserLoginForm()
                        context = {
                            'form': form,
                        }
                        messages.error(request, "Internship completed")
                        logout(request)
                        return render(request, "fossee_math_pages/login.html", context)
                    else:
                        return redirect(dashboard)
                        # return render(request, "fossee_math_pages/dashboard.html")

            except:

                form = UserLoginForm()
                context = {
                    'form': form,
                }
                messages.error(request, "Invalid Email or Password")
                return render(request, "fossee_math_pages/login.html", context)
        else:
            return render(request, "fossee_math_pages/login.html", {"form": form})
    else:
        form = UserLoginForm()
        return render(request, "fossee_math_pages/login.html", {"form": form})


@login_required
def staff_add_subtopic(request, id):
    form = add_subtopic()
    i_topic = Topic.objects.get(id=id)
    subtopics = Subtopic.objects.all()

    if request.method == 'POST':
        subtopic = request.POST['subtopic']
        topic_id = request.POST['id']
        u_id = request.user.id
        data = Subtopic(subtopic_name=subtopic, topic_id_id=topic_id, user_id_id=u_id)
        data.save()
        messages.success(request, 'Topic added with internship')
        i_topic = Topic.objects.get(id=id)

    context = {
        'form': form,
        'i_topic': i_topic,
        'subtopics': subtopics,
    }
    return render(request, 'fossee_math_pages/staff_add_subtopic.html', context)


@login_required
def staff_add_topics(request):
    form = add_topic()
    intern = Internship.objects.filter(internship_status='ACTIVE')
    topic = Topic.objects.all()

    if request.method == 'POST':
        topic = request.POST['topic']
        id = request.POST['id']
        u_id = request.user.id
        data = Topic(topic_name=topic, internship_id_id=id, user_id_id=u_id)
        data.save()
        messages.success(request, 'Topic added with internship')
        intern = Internship.objects.filter(internship_status='ACTIVE')
        topic = Topic.objects.all()

    context = {
        'form': form,
        'intern': intern,
        'topic': topic,
    }
    return render(request, 'fossee_math_pages/staff_add_topics.html', context)


@login_required
def staff_aprove_contents(request):
    subtopic = Subtopic.objects.all()
    assigned = AssignedTopics.objects.all()
    context = {
        'assigned': assigned,
        'subtopic': subtopic,
    }

    return render(request, 'fossee_math_pages/staff_aprove_contents.html', context)


@login_required
def staff_manage_intern(request):
    datas = UserDetails.objects.filter(user_role="INTERN")
    internship = Internship.objects.filter(internship_status='ACTIVE')
    topic = Topic.objects.all()

    assigned_topics = AssignedTopics.objects.all().select_related('topic_id')

    form = ManageIntern()
    if request.method == 'POST':
        int_id = request.POST["id"]
        obj = get_object_or_404(UserDetails, id=int_id)
        form = ManageIntern(request.POST or None, instance=obj)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            messages.success(request, "Changed")
            return redirect('staff_manage_intern')
        else:
            messages.error(request, "Error")
            return redirect('staff_manage_intern')

    context = {
        'datas': datas,
        'form': form,
        'internship': internship,
        'topic': topic,
        'assigned_topics': assigned_topics,
    }
    return render(request, 'fossee_math_pages/staff_manage_intern.html', context)


@login_required
def staff_assign_topic(request):
    user = User.objects.all()
    form = AssignTopic(user)
    inters = User.objects.filter(is_staff=False, is_superuser=False)
    intern = Internship.objects.filter(internship_status='ACTIVE')
    i_topic = Topic.objects.all()
    as_topic = AssignedTopics.objects.all()

    if request.method == "POST":
        intern_name = request.POST['user_id']
        topic = request.POST['topic_id']
        usr = UserDetails.objects.get(id=intern_name)
        temp1 = User.objects.get(id=usr.user_id_id)
        temp2 = Topic.objects.get(id=topic)
        if AssignedTopics.objects.filter(user_id=temp1).exists():
            messages.error(request, 'That intern has an assigned topic')
            return redirect('staff_assign_topic')
        elif AssignedTopics.objects.filter(topic_id=temp2).exists():
            messages.error(request, 'That topic is assigned alredy')
            return redirect('staff_assign_topic')
        else:
            data = AssignedTopics(user_id=temp1, topic_id=temp2)
            data.save()
            messages.success(request, 'Intern assigned with topic')

    context = {
        'interns': inters,
        'form': form,
        'intern': intern,
        'as_topic': as_topic,
        'i_topic': i_topic,
    }
    return render(request, 'fossee_math_pages/staff_assign_topic.html', context)


@login_required
def staff_view_interns(request):
    topics = AssignedTopics.objects.all()

    conxext = {
        'topics': topics,
    }
    return render(request, 'fossee_math_pages/staff_view_interns.html', conxext)


@login_required
def staff_view_internship(request):
    internship = Internship.objects.filter(internship_status='ACTIVE')
    topics = Topic.objects.all()
    subtopics = Subtopic.objects.all()

    context = {
        'internship': internship,
        'topics': topics,
        'subtopics': subtopics,
    }
    return render(request, 'fossee_math_pages/staff_view_internship.html', context)


@login_required
def staff_view_topic(request, s_id):
    subtopic = Subtopic.objects.get(id=s_id)
    data = Data.objects.filter(subtopic_id=subtopic.pk)

    context = {
        'subtopic': subtopic,
        'datas': data,
    }

    return render(request, 'fossee_math_pages/staff_view_topic.html', context)


@login_required
def staff_update_data(request, id):
    instance = Data.objects.get(id=id)
    subtopic = Subtopic.objects.get(id=instance.subtopic_id.pk)
    t_id = instance.subtopic_id.pk
    form = data(request.POST or None, instance=instance)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        return redirect('staff_view_topic', t_id)

    context = {
        'form': form,
        'subtopic': subtopic,
    }

    return render(request, 'fossee_math_pages/staff_update_data.html', context)


@login_required
def staff_aprove_data(request, id):
    instance = Data.objects.get(id=id)
    t_id = instance.subtopic_id.pk
    instance.data_status = "ACCEPTED"
    instance.save()
    return redirect('staff_view_topic', t_id)


@login_required
def staff_reject_data(request, id):
    print("hello")
    instance = Data.objects.get(id=id)
    t_id = instance.subtopic_id.pk
    instance.data_status = "REJECTED"
    instance.save()
    return redirect('staff_view_topic', t_id)


@login_required
def staff_delete_data(request, id):
    instance = Data.objects.get(id=id)
    t_id = instance.subtopic_id.pk
    instance.delete()
    return redirect('staff_view_topic', t_id)


@login_required
def user_logout(request):
    logout(request)
    return redirect('index')
