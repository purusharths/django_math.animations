import random
import re

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404,get_list_or_404
from django.shortcuts import render, redirect
from email_validator import validate_email, EmailNotValidError

from .forms import (AddUserForm1, AddUserForm2, UserLoginForm, AddInternship, ManageInternship, AddIntern, add_topic,
                    ManageIntern, add_subtopic, AssignTopic, data, AproveContents, Data_Verification)
from .models import (UserDetails, Internship, Intern, Topic, Subtopic, AssignedTopics, Data, DataVerification)


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
        data = Data.objects.get(subtopic_id_id=subtopic.pk)
        data_d = Data.objects.get(subtopic_id=data.pk)
        try:
            ver = DataVerification.objects.get(data_id=data_d.pk)
        except:
            ver = ""
    except Data.DoesNotExist:
        data = None

    context = {
        'subtopic': subtopic,
        'data': data,
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
    form = data()
    i=1
    user = request.user
    subtopic = Subtopic.objects.get(id=t_id)

    if request.method == 'POST':
        content = request.POST['data_content']
        reference = request.POST['data_reference']
        img = request.FILES.get('image')
        video = request.FILES.get('video')

        status = "WAITING"


        if Data.objects.filter(subtopic_id_id=t_id).exists():
            messages.success(request,"Data added successfuly")
            add_data = Data(data_content=content, data_reference=reference, data_status=status, data_image=img,
                            data_video=video, subtopic_id_id=t_id,
                            user_id_id=user.id)
            add_data.save()
            # print("error")
            # messages.error(request, "Data already exists")
            # return redirect(intern_view_topic)
        else:
            messages.success(request,"Data added successfully")
            add_data = Data(data_content=content, data_reference=reference, data_status=status, data_image=img, data_video=video, subtopic_id_id=t_id,
                            user_id_id=user.id)
            add_data.save()
    form = data

    context = {
        'form': form,
        'subtopic': subtopic,
        'i' : i,
    }
    return render(request, 'fossee_math_pages/intern_add_data.html', context)


@login_required
def intern_view_internship(request):
    internship = Internship.objects.filter(internship_status='ACTIVE')
    topics = Topic.objects.all()
    subtopics = Subtopic.objects.all()

    context = {
        'internship': internship,
        'topics': topics,
        'subtopics': subtopics,
    }
    return render(request, 'fossee_math_pages/intern_view_internship.html', context)


@login_required
def intern_edit_data(request, e_id):
    post = get_list_or_404(Data,subtopic_id_id = e_id)
    datas = Data.objects.filter(subtopic_id_id = e_id)
    sub = Data.objects.filter(subtopic_id_id=e_id)
    print("sub")
    form = data


    listing = Data.objects.all();
    paginator = Paginator(listing,2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    for i in page_obj:
        if form.is_valid:
            form.data_content = i.data_content
    #content = page_obj.data_content;
    #xprint(content)
    return render(request, 'fossee_math_pages/intern_edit_data.html', {'page_obj': page_obj,'form':form})
    for i in sub:
        print(i.data_reference)
    form = data
    for i in datas:
        print(i.data_content)
    context = {
        'data' : datas,
        'form' : form
    }
    if request.user:
        form = data
       # form = data(instance = post)
        context ={
            'form' : form,
            'sub' : sub
        }
    return render(request, 'fossee_math_pages/intern_edit_data.html', context)

    if request.method == 'POST':
        form = data(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            form = data
            messages.success(request, "Editing was successfull")
    return render(request, 'fossee_math_pages/intern_edit_data.html',context)
    # post = get_object_or_404(Data, subtopic_id_id=e_id)
    # sub = Data.objects.filter(subtopic_id_id=e_id)
    # subtopic = Subtopic.objects.filter(id=sub.subtopic_id_id)
    #
    # if request.user:
    #     form = data
    #     form = data(instance=post)
    #     context = {
    #         'internship': internship,
    #         'form': form,
    #         'subtopic': subtopic,
    #         'content': sub.data_content,
    #         'reference': sub.data_reference,
    #     }
    #
    #     if request.method == 'POST':
    #         form = data(request.POST, request.FILES, instance=post)
    #         if form.is_valid():
    #             post = form.save(commit=False)
    #             post.save()
    #             form = data
    #             messages.success(request, "Editing was successfull")
    #             return redirect(intern_view_topic)
    #
    #     return render(request, 'fossee_math_pages/intern_edit_data.html', context)


@login_required
def intern_view_data(request, v_id):
    print(v_id)
    i=[1,2]
    if Data.objects.filter(subtopic_id_id=v_id).exists():
        print("haii")
    topic = Data.objects.filter(subtopic_id_id=v_id)
    int_name =topic[0].subtopic_id.topic_id.internship_id
    topic_name = topic[0].subtopic_id.topic_id
    sub_topic = topic[0].subtopic_id
    status = topic[0].data_status
    context = {
        'topic': topic,
        'int_name':int_name,
        'topic_name' : topic_name,
        'sub_topic':sub_topic,
        'status':status
         }
    print(topic[0].subtopic_id.topic_id.internship_id)
    return render(request, 'fossee_math_pages/intern_view_data.html', context)
    # try:
    #
    #     topic = Data.objects.get(subtopic_id_id=v_id)
    #     context = {
    #         'topic': topic
    #     }
    #     print(topic.internship_id)
    #     return render(request, 'fossee_math_pages/intern_view_data.html', context)
    #
    # except:
    #     return render(request, 'fossee_math_pages/intern_view_data.html')


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
                    return render(request, "fossee_math_pages/dashboard.html")
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
                        return render(request, "fossee_math_pages/dashboard.html")

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
    data_f = Data.objects.filter(data_status='WAITING')
    sub_f = Subtopic.objects.all()
    topic_f = Topic.objects.all()
    internship_f = Internship.objects.filter(internship_status='ACTIVE')
    user_details = UserDetails.objects.filter(user_role='INTERN')
    aproved = Data.objects.filter(data_status='ACCEPTED')
    rejected = Data.objects.filter(data_status='REJECTED')
    changes = Data.objects.filter(data_status='UNDER REVIEW')
    context = {
        'datas': data_f,
        'sub_f': sub_f,
        'topic_f': topic_f,
        'internship_f': internship_f,
        'user_details': user_details,
        'aproved': aproved,
        'rejected': rejected,
        'changes': changes,
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
def staff_add_reviever(request, s_id):
    data_info = Data.objects.get(id=s_id)
    interndhip_info = Internship.objects.filter(internship_status='ACTIVE')
    assigned_topic = AssignedTopics.objects.get(user_id_id=data_info.user_id_id)
    verify = Data_Verification()
    ver = ""

    if request.POST:
        try:
            ver = DataVerification.objects.get(data_id=s_id)
            messages.error(request, 'Data exists')
        except:
            verifier = request.POST['dataverification_verifier']
            mentor = request.POST['dataverification_mentor']
            mentor = User.objects.get(id=mentor)
            daa = Data.objects.get(pk=s_id)
            data = DataVerification(dataverification_verifier=verifier, dataverification_mentor=mentor, data_id=daa)
            data.save()
            ver = DataVerification.objects.get(data_id=s_id)
            messages.success(request, 'Data Added Successfully')

    context = {
        'form': verify,
        'ver': ver,
        'data_info': data_info,
        'interndhip_info': interndhip_info,
        'assigned_topic': assigned_topic,
    }

    return render(request, 'fossee_math_pages/staff_add_reviewer.html', context)


@login_required
def staff_view_topic(request, s_id):
    data_info = Data.objects.get(id=s_id)
    post = get_object_or_404(Data, id=s_id)
    interndhip_info = Internship.objects.filter(internship_status='ACTIVE')
    assigned_topic = AssignedTopics.objects.get(user_id_id=data_info.user_id_id)
    subtopic = Subtopic.objects.get(id=data_info.subtopic_id_id)
    print(data_info.data_reference)

    try:
        verify = DataVerification.objects.get(data_id=s_id)
    except:
        verify = ""

    if request.user:
        form = AproveContents
        form = AproveContents(instance=post)
        context = {
            'ver': verify,
            'data_info': data_info,
            'internship_info': interndhip_info,
            'assigned_topic': assigned_topic,
            'subtopic': subtopic,
            'form': form,
        }

        if request.method == "POST":
            form = AproveContents(request.POST, request.FILES, instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                post.save()
                form = AproveContents
                data_info = Data.objects.get(id=s_id)
                interndhip_info = Internship.objects.filter(internship_status='ACTIVE')
                assigned_topic = AssignedTopics.objects.get(user_id_id=data_info.user_id_id)
                subtopic = Subtopic.objects.get(id=data_info.subtopic_id_id)
                context = {'form': form,
                           'data_info': data_info,
                           'internship_info': interndhip_info,
                           'assigned_topic': assigned_topic,
                           'subtopic': subtopic,
                           }
                return render(request, 'fossee_math_pages/staff_view_topic.html', context)

        return render(request, 'fossee_math_pages/staff_view_topic.html', context)


def user_logout(request):
    logout(request)
    return redirect('index')
