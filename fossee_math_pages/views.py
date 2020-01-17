import random
import re
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from email_validator import validate_email, EmailNotValidError
from django.core.paginator import Paginator
from .forms import (AddUserForm1, AddUserForm2, UserLoginForm, AddInternship, ManageInternship, AddIntern, add_topic,
                    ManageIntern, add_subtopic, AssignTopic, data)
from .models import UserDetails, Internship, Intern, Topic, Subtopic, AssignedTopics, Data


# def index(request):
#     return render(request, "fossee_math_pages/index.html")


# def internship(request):
#     return render(request, "fossee_math_pages/internship.html")


# def topics(request):
#     try:
#         details = AddUser.objects.filter(role='INTERN')
#         resources = data.objects.all()
#         context = {
#             'resources': resources,
#             'usr': details,
#         }
#         return render(request, 'fossee_math_pages/topics.html', context)
#     except:
#         return render(request, "fossee_math_pages/topics.html")


# def is_superuser(user):
#     return user.is_superuser


# @login_required
# def dashboard(request):
#     if request.user:
#         current_user = request.user
#         intern_count = AddUser.objects.filter(role='INTERN').count()
#         staff_count = AddUser.objects.filter(role='STAFF').count()
#         # for admin
#         status_active = AddUser.objects.filter(status='ACTIVE').count()
#         status_inactive = AddUser.objects.filter(status='INACTIVE').count()
#         status_suspended = AddUser.objects.filter(status='SUSPENDED').count()
#         # for intern 
#         date_joined = User.objects.filter(id=current_user.id)
#         total_proposals_intern = data.objects.filter(id=current_user.id).count()
#         proposal_status_intern = data.objects.filter(id=current_user.id,aproval_ststus=True).count()
#         # for staff
#         total_proposals = data.objects.all().count()
#         proposal_status_true = data.objects.filter(aproval_ststus=True).count()
#         proposal_status_false = data.objects.filter(aproval_ststus=False).count()
#         context = {

#             'intern_count' : intern_count,
#             'staff_count' : staff_count,
#             'status_active' :status_active,
#             'status_inactive' : status_inactive,
#             'status_suspended' : status_suspended,
#             'date_joined' : date_joined,
#             'total_proposals_intern' : total_proposals_intern,
#             'proposal_status_intern' : proposal_status_intern,
#             'total_proposals' : total_proposals,
#             'proposal_status_true' : proposal_status_true,
#             'proposal_status_false' : proposal_status_false
#         }

#         return render(request, "fossee_math_pages/dashboard.html", context)
#     else:

#         return redirect('logout')


# def manage_intern(request):
#     details = AddUser.objects.filter(role='INTERN')
#     users = User.objects.all()
#     print("hai")
#     context = {
#         'users': users,
#         'details': details,
#     }
#     if request.method == 'POST':
#         # register user
#         u_id = request.POST['id']
#         option = request.POST['option_select']
#         AddUser.objects.filter(user_id=u_id).update(status=option)

#     return render(request, 'fossee_math_pages/manage_intern.html', context)


# @login_required
# def aprove_contents(request):
#     data_aproval = data.objects.filter(aproval_ststus='PENDING').order_by('-user_id')
#     inters = AddUser.objects.filter(role='INTERNS')
#     context = {
#         'data': data_aproval,
#         'inters': inters,
#     }
#     return render(request, 'fossee_math_pages/aprove_contents.html', context)


# @login_required
# def add_details(request):
#     form = add_data
#     user=User.objects.get(pk=request.user.id)
#     if request.method == 'POST':
#         form = add_data(request.POST, request.FILES)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.user_id = user
#             post.aproval_ststus = 'PENDING'
#             post.save()
#             form = add_data
#             return render(request, 'fossee_math_pages/intern_add_data.html', {'form': form})
#     return render(request, 'fossee_math_pages/intern_add_data.html', {'form': form})


# @login_required
# def view_details(request):
#     try:
#         usr = request.user
#         details = AddUser.objects.get(user_id=usr.id)
#         resources = data.objects.filter(user_id=usr.id)
#         context = {
#             'resources': resources,
#             'usr': details,
#         }
#         return render(request, 'fossee_math_pages/intern_view_topic.html', context)
#     except:
#         return render(request, 'fossee_math_pages/intern_view_topic.html')


# @login_required
# def view_data(request, view_id):
#     try:
#         topic = data.objects.get(id=view_id)
#         context = {
#             'topic': topic
#         }
#         print(topic.text)
#         return render(request, 'fossee_math_pages/intern_view_data.html', context)

#     except:
#         return render(request, 'fossee_math_pages/intern_view_data.html')


# def viewdata(request, view_id):
#     try:
#         topic = data.objects.get(id=view_id)
#         context = {
#             'topic': topic
#         }
#         print(topic.text)
#         return render(request, 'fossee_math_pages/data.html', context)
#     except:
#         return render(request, 'fossee_math_pages/data.html')


# @login_required
# def edit_data(request,edit_id):
#     print(edit_id)
#     post = get_object_or_404(data,id = edit_id)
#     sub = data.objects.get(id = edit_id);
#     context ={
#         'subtop' :sub.subtopic,
#     }

#     if request.user:
#         form = add_data
#         form = add_data(instance=post)
#         if request.method == 'POST':
#             form = add_data(request.POST, request.FILES, instance=post)
#             if form.is_valid():
#                 post = form.save(commit=False)
#                 post.save()
#                 form = add_data
#                 return render(request, 'fossee_math_pages/intern_edit_data.html', {'form': form})
#     return render(request, 'fossee_math_pages/intern_edit_data.html', {'form': form,'context':context})


# class AddUserView(AddUser):
#     def create_user(self, request, *args, **kwargs):
#         name = self.name
#         email = self.email
#         password = random.randint(0, 99999999)
#         user = User.objects.create_user(name, email, password)
#         user.save(using=self._db)
#         return user

@login_required
def admin_add_internship(request):
    form = AddInternship()
    if request.method == 'POST':
        internship_topic = request.POST['internship_topic']
        internship_thumbnail = request.POST['internship_thumbnail']
        internship_status = request.POST['internship_status']
        if Internship.objects.filter(internship_topic=internship_topic).exists():
            messages.error(request, 'That internship already exist')
            return redirect('admin_add_internship')
        try:
            data = Internship(internship_topic=internship_topic, internship_thumbnail=internship_thumbnail,
                              internship_status=internship_status)
            data.save()
            messages.success(request, 'Internship added')
            return redirect('admin_add_internship')
        except:
            messages.error(request, 'Some error occured')
            return redirect('admin_add_internship')
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
        temp1 = User.objects.get(username=usr)
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
def admin_view_intern(request):
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
            return redirect('admin_view_intern')
        else:
            messages.error(request, "Error")
            return redirect('admin_view_intern')

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


def home_topics(request):
    interships = Internship.objects.filter(internship_status='COMPLETED')
    context = {
        'internship': interships,
    }
    return render(request, 'fossee_math_pages/home_topics.html', context)


def home_view_data(request):
    return render(request, 'fossee_math_pages/home_view_data.html')


def index(request):
    return render(request, 'fossee_math_pages/index.html')


@login_required
def intern_add_data(request, t_id):
    form = data
    internship = Internship.objects.get(internship_status='ACTIVE')
    # Subtopic id
    print(t_id)
    user = request.user
    print(user.id)  # user id
    if request.method == 'POST':
        content = request.POST['data_content']
        reference = request.POST['data_reference']
        status = "Waiting"
        add_data = Data(data_content=content, data_reference=reference, data_status=status, subtopic_id_id=t_id,
                        user_id_id=user.id)
        add_data.save()

    context = {
        'form': form,
        'internship': internship,
    }
    return render(request, 'fossee_math_pages/intern_add_data.html', context)


def intern_view_internship(request):
    internship = Internship.objects.get(internship_status='ACTIVE')
    topics = Topic.objects.filter(internship_id=internship.pk)
    subtopics = Subtopic.objects.all()

    context = {
        'internship': internship,
        'topics': topics,
        'subtopics': subtopics,
    }
    return render(request, 'fossee_math_pages/intern_view_internship.html', context)


def intern_edit_data(request):
    return render(request, 'fossee_math_pages/intern_edit_data.html')


def intern_view_data(request):
    return render(request, 'fossee_math_pages/intern_view_data.html')


def intern_view_topic(request):
    internship = Internship.objects.get(internship_status='ACTIVE')
    assigned_topic = AssignedTopics.objects.get(user_id=request.user.id)
    subtopic = Subtopic.objects.filter(topic_id=assigned_topic.topic_id)

    context = {
        'internship': internship,
        'assigned': assigned_topic,
        'subtopic': subtopic,
    }
    return render(request, 'fossee_math_pages/intern_view_topic.html', context)


def internship(request):
    return render(request, 'fossee_math_pages/internship.html')


def user_login(request):
    user = request.user

    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = form.authenticate_user()
            login(request, user)
            return render(request, "fossee_math_pages/dashboard.html")
        else:
            return render(request, "fossee_math_pages/login.html", {"form": form})
    else:
        form = UserLoginForm()
        return render(request, "fossee_math_pages/login.html", {"form": form})


@login_required
def staff_add_subtopic(request, id):
    form = add_subtopic()
    intern = Internship.objects.get(internship_status='ACTIVE')
    i_topic = Topic.objects.get(id=id)
    subtopics = Subtopic.objects.filter(topic_id_id=id)

    if request.method == 'POST':
        subtopic = request.POST['subtopic']
        topic_id = id
        u_id = request.user.id
        data = Subtopic(subtopic_name=subtopic, topic_id_id=topic_id, user_id_id=u_id)
        data.save()
        messages.success(request, 'Topic added with internship')
        intern = Internship.objects.get(internship_status='ACTIVE')
        i_topic = Topic.objects.get(id=id)

    context = {
        'form': form,
        'intern': intern,
        'i_topic': i_topic,
        'subtopics': subtopics,
    }
    return render(request, 'fossee_math_pages/staff_add_subtopic.html', context)


@login_required
def staff_add_topics(request):
    form = add_topic()
    intern = Internship.objects.get(internship_status='ACTIVE')
    i_topic = Topic.objects.filter(internship_id_id=intern.id)
    subtopics = Subtopic.objects.all()

    if request.method == 'POST':
        topic = request.POST['topic']
        intern_id = intern.id
        u_id = request.user.id
        data = Topic(topic_name=topic, internship_id_id=intern_id, user_id_id=u_id)
        data.save()
        messages.success(request, 'Topic added with internship')
        intern = Internship.objects.get(internship_status='ACTIVE')
        i_topic = Topic.objects.filter(internship_id_id=intern.id)

    context = {
        'form': form,
        'intern': intern,
        'i_topic': i_topic,
        'subtopics': subtopics,
    }
    return render(request, 'fossee_math_pages/staff_add_topics.html', context)


def staff_aprove_contents(request):
    interns = UserDetails.objects.filter(user_role='INTERN')
    user = User.objects.all()
    internship = Internship.objects.all()
    data = Data.objects.all()
    assigned = AssignedTopics.objects.all()
    topic = Topic.objects.all()

    context = {
        'interns': interns,
        'user': user,
        'internship': internship,
        'data': data,
        'assigned': assigned,
        'topic': topic,
    }
    return render(request, 'fossee_math_pages/staff_aprove_contents.html', context)


@login_required
def staff_manage_intern(request):
    datas = UserDetails.objects.filter(user_role="INTERN")
    internship = Internship.objects.get(internship_status='ACTIVE')
    topic = Topic.objects.filter(internship_id=internship.pk)

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
    intern = Internship.objects.get(internship_status='ACTIVE')
    i_topic = Topic.objects.all()
    as_topic = AssignedTopics.objects.all()

    if request.method == "POST":
        intern_name = request.POST['user_id']
        topic = request.POST['topic_id']
        temp1 = User.objects.get(id=intern_name)
        temp2 = Topic.objects.get(id=topic)
        if AssignedTopics.objects.filter(user_id=intern_name).exists():
            messages.error(request, 'That intern has an assigned topic')
            return redirect('staff_assign_topic')
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


def staff_view_interns(request):
    return render(request, 'fossee_math_pages/staff_view_interns.html')


def staff_view_internship(request):
    internship = Internship.objects.get(internship_status='ACTIVE')
    topics = Topic.objects.filter(internship_id=internship.pk)
    subtopics = Subtopic.objects.all()

    context = {
        'internship': internship,
        'topics': topics,
        'subtopics': subtopics,
    }
    return render(request, 'fossee_math_pages/staff_view_internship.html', context)


def staff_view_topic(request):
    return render(request, 'fossee_math_pages/staff_view_topic.html')


def user_logout(request):
    logout(request)
    return redirect('index')
