import hashlib
import uuid
import random
import re
import string

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, EmailMessage
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.timezone import now
from email_validator import validate_email, EmailNotValidError

from .forms import (AddUserForm1, AddUserForm2, UserLoginForm, AddInternship, ManageInternship, add_topic,
                    ManageIntern, add_subtopic, data, EditMedia, AddContributor, imageFormatting, topicOrder,
                    subtopicOrder, AssignTopic, addContributor, sendMessage, )
from .models import (UserDetails, Internship, Topic, Subtopic, Contributor, Data, ImageFormatting, HomeImages, Messages)
from .tokens import account_activation_token


@login_required
def add_internship(request):
    if request.user.is_superuser:
        form = AddInternship()
        internship = Internship.objects.all()
        if request.method == 'POST':
            internship_topic = request.POST['internship_topic']
            form = AddInternship(request.POST, request.FILES)
            if Internship.objects.filter(internship_topic=internship_topic).exists():
                messages.error(request, 'That internship already exist')
                return redirect('add-internship')
            if form.is_valid():
                obj = form.save(commit=False)
                obj.save()
                current_instance = Internship.objects.get(pk=obj.pk)
                current_instance.internship_url = '-'.join(str(internship_topic).lower().split())
                current_instance.save()
                messages.success(request, 'Internship added')
                return redirect('add-internship')
            else:
                messages.error(request, 'An error occured! Contact the admin!')
                return redirect('add-internship')
        form = AddInternship()
        context = {
            'form': form,
            'internship': internship,
        }
        return render(request, 'fossee_math_pages/add-internship.html', context)
    else:
        return redirect('dashboard')


@login_required
def manage_internship(request):
    if request.user.is_superuser:
        internship = None
        form = ManageInternship

        if request.method == 'POST':
            if "search_internship" in request.POST:
                internship = Internship.objects.get(pk=request.POST['search_internship'])
            else:
                int_id = request.POST["id"]
                obj = get_object_or_404(Internship, id=int_id)
                form = ManageInternship(request.POST or None, instance=obj)
                if form.is_valid():
                    obj = form.save(commit=False)
                    obj.save()
                    messages.success(request, "Changed")
                    return redirect('manage-internship')
                else:
                    messages.error(request, "Error")
                    return redirect('manage-internship')

        internship_all = Internship.objects.all()

        context = {
            'internship': internship,
            'internship_all': internship_all,
            'form': form
        }
        return render(request, 'fossee_math_pages/manage-internship.html', context)
    else:
        return redirect('dashboard')


@login_required
def add_users(request):
    if request.user.is_superuser:
        datas = UserDetails.objects.all()
        user_contains_query = request.GET.get('title_contains')
        if user_contains_query != '' and user_contains_query is not None:
            datas = UserDetails.objects.filter(user_id__username__contains=user_contains_query)
        if user_contains_query == "STAFF" or user_contains_query == "staff":
            datas = UserDetails.objects.filter(user_role="STAFF")
        if user_contains_query == "INTERN" or user_contains_query == "intern":
            datas = UserDetails.objects.filter(user_role="INTERN")

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
            user_status = 'INACTIVE'

            regex = re.compile(r'[@_!#$%^&*()<>?/\|}{~:]')
            if User.objects.filter(email=email).exists():
                messages.error(request, 'That email is being used')
                return redirect('add-users')
            if User.objects.filter(username=username).exists():
                messages.error(request, 'That username is being used')
                return redirect('add-users')
            if firstname.isdigit():
                messages.error(request, 'Firstname cannot have numbers')
                return redirect('add-users')
            if regex.search(firstname):
                messages.error(request, 'Firstname cannot have special characters')
                return redirect('add-users')
            if lastname.isdigit():
                messages.error(request, 'Lastname cannot have numbers')
                return redirect('add-users')
            if regex.search(lastname):
                messages.error(request, 'Lastname cannot have special characters')
                return redirect('add-users')
            Pattern = re.compile(r"(/+91)?[7-9][0-9]{9}")
            if Pattern.match(user_phone):
                messages.error(request, 'Phone number error')
                return redirect('add-users')
            try:
                v = validate_email(email)
                val_email = v["email"]
            except EmailNotValidError as e:
                messages.error(request, 'Invalid Email ID')
                return redirect('add-users')

            try:
                password = ''.join([random.choice(string.ascii_letters + string.digits) for K in range(10)])
                passwordstr = str(password)
                user = User.objects.create_user(username=username, email=email, password=password, first_name=firstname,
                                                last_name=lastname, is_active=False)
                u_id = User.objects.get(username=username)

                if user_role == 'INTERN':
                    addusr = UserDetails(user_id=u_id, user_phone=user_phone, user_role=user_role,
                                         user_temp_password=password, user_status=user_status, user_email=email)
                    addusr.save()
                if user_role == 'STAFF':
                    user.is_staff = True
                    user.save()
                    addusr = UserDetails(user_id=u_id, user_phone=user_phone, user_role=user_role,
                                         user_temp_password=password, user_status=user_status, user_email=email)
                    addusr.save()

                current_site = get_current_site(request)
                mail_subject = 'Activate your FOSSEE MATH USER account'
                message = render_to_string('fossee_math_pages/activate_user.html', {
                    'user': email,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                    'pass': password,
                })
                to_email = email
                email = EmailMessage(mail_subject, message, to=[to_email])
                email.send()
            except:
                usr = User.objects.get(username=email)
                usr.delete()
                messages.error(request, 'Some error occured !')
                return redirect('add-users')
            messages.success(request, 'User Added!')
            return redirect('add-users')

        paginator = Paginator(datas, 25)  # Show 25 contacts per page.

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'datas': page_obj,
            'form': form,
            'sub_form': sub_form,
        }
        return render(request, 'fossee_math_pages/add-users.html', context)
    else:
        return redirect('dashboard')


@login_required
def dashboard(request):
    return render(request, 'fossee_math_pages/dashboard.html')


def contents(request, internship):
    internship_details = Internship.objects.get(internship_url=internship)
    id = internship_details.pk
    details = Internship.objects.get(id=id)
    topics = Topic.objects.filter(internship_id_id=id)
    subtopics = Subtopic.objects.all()

    if request.POST:
        search_contains_query = request.POST.get('title_contains')
        return home_search_results(request, search_contains_query)

    context = {
        'details': details,
        'topics': topics,
        'subtopics': subtopics,
    }
    return render(request, 'fossee_math_pages/contents.html', context)


def home_details(request, internship, topic, subtopic):
    selected_internship = Internship.objects.get(internship_url=internship)
    subtopic_request = Subtopic.objects.filter(topic_id__internship_id_id=selected_internship.pk).filter(
        topic_id__topic_url=topic).get(
        subtopic_url=subtopic)
    id = subtopic_request.pk
    subtopic_details = Subtopic.objects.get(id=id)
    contributor = ""
    ver = ""
    try:
        data = Data.objects.all()
        imagesize = ImageFormatting.objects.all()
    except Data.DoesNotExist:
        data = None
        imagesize = None

    try:
        contributor = Contributor.objects.get(topic_id=subtopic_details.topic_id)
    except:
        contributor = None

    context = {
        'subtopic': subtopic_details,
        'datas': data,
        'contributor': contributor,
        'ver': ver,
        'imagesize': imagesize,
    }
    return render(request, 'fossee_math_pages/home_details.html', context)


def index(request):
    search_contains_query = request.GET.get('title_contains')
    images = HomeImages.objects.all()  # change

    interships = Internship.objects.filter(internship_status='COMPLETED')

    if search_contains_query != '' and search_contains_query is not None:
        return home_search_results(request, search_contains_query)

    context = {
        'internship': interships,
        'images': images,
    }

    return render(request, 'fossee_math_pages/index.html', context)


def home_search_results(request, search_contains_query):
    datas = ""
    datass = ""
    page_obj = ""
    topic = Subtopic.objects.all()

    datas = Subtopic.objects.filter(subtopic_name__icontains=search_contains_query)
    datass = Subtopic.objects.filter(topic_id__topic_name__icontains=search_contains_query)

    if datas:
        paginator = Paginator(datas, 15)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

    if datass:
        paginator = Paginator(datass, 15)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

    data_search = Data.objects.all()

    context = {
        'datas': page_obj,
        'topic': topic,
        'querry': search_contains_query,
        'data_search': data_search,
    }
    return render(request, 'fossee_math_pages/home_search_results.html', context)


@login_required
def add_submission_subtopic(request, st_id):
    if request.user.is_authenticated and not request.user.is_staff and not request.user.is_superuser:
        user = request.user
        form = data

        subtopic = Subtopic.objects.get(subtopic_hash=st_id)
        t_id = subtopic.pk
        if subtopic.assigned_user_id.id == request.user.id:
            if request.method == 'POST':
                content = request.POST.get('data_content')
                img = request.FILES.get('image')
                video = request.FILES.get('video')
                caption_image = request.POST.get('caption_image')
                caption_video = request.POST.get('caption_video')
                caption = None

                if subtopic.assigned_user_id.id == request.user.id:
                    if img is None and video is None:
                        if content == "" or content == " ":
                            if content.strip() == '':
                                messages.error(request, "Fill any one of the field")
                                return redirect('add-submission-subtopic', st_id)

                    if img is None and content.strip() == '':
                        caption = caption_video
                        video_file = str(video)
                        if not video_file.lower().endswith(('.mp4', '.webm')):
                            messages.error(request, 'Inavalid File Type for Video')
                            return redirect('add-submission-subtopic', st_id)

                    if video is None and content.strip() == '':
                        caption = caption_image
                        image = str(img)
                        if not image.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                            messages.error(request, 'Inavalid File Type for Image')
                            return redirect('add-submission-subtopic', st_id)

                    if img and video is None:
                        caption = None

                    add_data = Data(data_content=content, data_image=img,
                                    data_video=video, data_caption=caption, subtopic_id_id=t_id)
                    add_data.data_modification_date = now()
                    add_data.save()
                    sub = Subtopic.objects.get(pk=t_id)
                    sub.subtopic_modification_date = now()
                    sub.save()
                    current_data = Data.objects.get(pk=add_data.pk)
                    # hashtext = str(current_data.pk) + '-' + str(request.user.pk)
                    # hash_result = hashlib.md5(hashtext.encode())
                    # add_data.data_hash = hash_result.hexdigest()
                    uuid_hash = uuid.uuid4()
                    add_data.data_hash = str(uuid_hash)
                    add_data.save()

                    if img != "" or img != " ":
                        imgformat = ImageFormatting(data_id_id=add_data.pk, image_width='50%', image_height='50%')
                        imgformat.save()

            e_data = Data.objects.filter(subtopic_id=t_id)
            imagesize = ImageFormatting.objects.all()
            subtopic = Subtopic.objects.get(id=t_id)

            try:
                last_modified = sorted([dta.data_modification_date for dta in e_data])[-1].strftime(
                    '%B %d, %Y %H:%M:%S (%A)')
            except IndexError:
                last_modified = "No modifications"

            context = {
                'topic': e_data,
                'form': form,
                'subtopic': subtopic,
                'imagesize': imagesize,
                'last_modified': last_modified,
            }

            return render(request, 'fossee_math_pages/add-submission-subtopic.html', context)
        else:
            messages.error(request,'Illegal action')
            return redirect('dashboard')
    else:
        return redirect('dashboard')


@login_required
def edit_text(request, t_id, id):
    if request.user.is_authenticated and not request.user.is_superuser:
        instance = Data.objects.get(data_hash=id)
        subtopic = Subtopic.objects.get(id=instance.subtopic_id.pk)
        t_id = instance.subtopic_id.subtopic_hash
        if (subtopic.assigned_user_id.id == request.user.id) or request.user.is_staff:
            form = data(request.POST or None, instance=instance)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.save()
                if request.user.is_staff:
                    return redirect('review-submissions-subtopic', t_id)
                else:
                    return redirect('add-submission-subtopic', t_id)
        else:
            return redirect('dashboard')

        context = {
            'form': form,
            'subtopic': subtopic,
        }

        return render(request, 'fossee_math_pages/edit-text.html', context)
    else:
        return redirect('dashboard')


@login_required
def edit_media(request, t_id, id):
    if request.user.is_authenticated and not request.user.is_staff and not request.user.is_superuser:
        instance = Data.objects.get(data_hash=id)
        subtopic = Subtopic.objects.get(id=instance.subtopic_id.pk)
        if request.user.id == subtopic.assigned_user_id.id:
            t_id = instance.subtopic_id.subtopic_hash
            form = EditMedia(request.POST or None, instance=instance)
            if request.POST:
                if form.is_valid():
                    content = request.POST.get('data_content')
                    img = request.FILES.get('data_image')
                    video = request.FILES.get('data_video')
                    instance = Data.objects.get(data_hash=id)
                    if img is None and video is None:
                        if content.strip() == '':
                            messages.error(request, "Fill any one of the field")
                            return redirect('edit-media', t_id, id)

                    if img is None and content.strip() == '':
                        content = ""
                        img = ""
                        video_file = str(video)
                        if not video_file.lower().endswith(('.mp4', '.webm')):
                            messages.error(request, 'Inavalid File Type for Video')
                            return redirect('edit-media', t_id, id)

                    if video is None and content.strip() == '':
                        content = ""
                        video = ""
                        image = str(img)
                        if not image.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                            messages.error(request, 'Inavalid File Type for Image')
                            return redirect('edit-media', t_id, id)

                    instance.data_content = content
                    instance.data_image = img
                    instance.data_video = video
                    instance.data_caption = ""
                    instance.data_modification_date = now()
                    instance.save()
                    sub = Subtopic.objects.get(pk=instance.subtopic_id.pk)
                    sub.subtopic_modification_date = now()
                    sub.save()
                    return redirect('add-submission-subtopic', t_id)

            context = {
                'form': form,
                'subtopic': subtopic,
            }
            return render(request, 'fossee_math_pages/edit-media.html', context)
        else:
            messages.error(request,'Illegal action')
            return redirect('dashboard')
    else:
        return redirect('dashboard')


@login_required
def edit_image(request, t_id, id):
    if request.user.is_authenticated and not request.user.is_superuser:
        image = Data.objects.get(data_hash=id)
        try:
            image_size = ImageFormatting.objects.get(data_id_id=image.pk)
            form = imageFormatting(instance=image_size)
        except:
            image_size = None
            form = imageFormatting()

        if request.POST:
            image_height = request.POST.get('image_height')
            image_width = request.POST.get('image_width')
            caption = request.POST.get('image_caption')

            temp = re.findall(r'\d+', image_height)
            res = list(map(int, temp))
            if res[0] >= 100:
                image_height = "500px"

            temp = re.findall(r'\d+', image_height)
            res = list(map(int, temp))
            if res[0] >= 100:
                image_width = "900px"

            obj = ImageFormatting.objects.get(data_id_id=image.pk)
            obj.image_height = image_height
            obj.image_width = image_width
            obj.image_caption = caption
            obj.save()
            if request.user.is_staff:
                return redirect('edit-image-staff', t_id, id)
            else:
                return redirect('edit-image', t_id, id)

        context = {
            'image': image,
            'image_size': image_size,
            'form': form,
        }

        return render(request, 'fossee_math_pages/edit-image.html', context)
    else:
        return redirect('dashboard')


@login_required
def delete_data(request, id):
    if request.user.is_authenticated and not request.user.is_superuser:
        instance = Data.objects.get(data_hash=id)
        if instance.subtopic_id.assigned_user_id.id == request.user.id:
            t_id = instance.subtopic_id.subtopic_hash
            try:
                image = ImageFormatting.objects.get(data_id=instance.id)
                image.delete()
                instance.delete()
            except:
                instance.delete()
            return redirect('add-submission-subtopic', t_id)

        elif request.user.is_staff:
            t_id = instance.subtopic_id.subtopic_hash
            try:
                image = ImageFormatting.objects.get(data_id=instance.id)
                image.delete()
                instance.delete()
            except:
                instance.delete()
            return redirect('review-submissions-subtopic', t_id)

        else:
            return redirect('dashboard')

    else:
        return redirect('dashboard')


@login_required
def add_submission(request):
    if request.user.is_authenticated and not request.user.is_staff and not request.user.is_superuser:
        assigned_topic = Subtopic.objects.filter(assigned_user_id_id=request.user.id)

        context = {
            'assigned_topic': assigned_topic,
        }
        return render(request, 'fossee_math_pages/add-submission.html', context)
    else:
        return redirect('dashboard')


def internship(request):
    return render(request, 'fossee_math_pages/internship.html')


def password_change(request):
    form = PasswordChangeForm(user=request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Password Changes Successfully !')
            return redirect(dashboard)

    context = {
        'form': form,
    }
    return render(request, "fossee_math_pages/password-change.html", context)


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
                    user = UserDetails.objects.get(user_id=request.user.id)
                    if user.user_status == 'INACTIVE':
                        messages.error(request,"Your login credentials are invalid! Please contact the admin")
                        logout(request)
                        form = UserLoginForm()
                        context = {
                            'form': form,
                        }
                        return render(request, "fossee_math_pages/login.html", context)
                    else:
                        return redirect(dashboard)
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
def add_subtopics(request, i_id, t_id):
    if request.user.is_staff:
        form = add_subtopic()
        rearrange_subtopic = subtopicOrder()
        i_topic = Topic.objects.get(topic_url=t_id, internship_id__internship_url=i_id)
        subtopics = Subtopic.objects.all().order_by('subtopic_order')

        if request.method == 'POST':
            if "subtopic_order" in request.POST:
                subtopicoder = request.POST['subtopic_order']
                subtopic_id = request.POST['subtopicid']
                obj = Subtopic.objects.get(pk=subtopic_id)
                obj.subtopic_order = subtopicoder
                obj.save()
            else:
                subtopic = request.POST['subtopic']
                topic_id = request.POST['id']

                if subtopic.strip() == '':
                    messages.error(request, "Fill the field")
                    return redirect('add-subtopics', t_id)
                else:
                    obj = Subtopic.objects.filter(topic_id__topic_url=t_id,
                                                  topic_id__internship_id_id=i_topic.internship_id).order_by(
                        'subtopic_order').last()
                    if obj:
                        order = obj.subtopic_order
                    else:
                        order = 0
                    try:
                        Subtopic.objects.get(subtopic_name=subtopic, topic_id_id=topic_id)
                        messages.error(request, "Subtopic exists !")
                    except:
                        order = order + 1
                        data = Subtopic(subtopic_name=subtopic, topic_id_id=topic_id, subtopic_order=order)
                        data.save()
                        current_subtopic = Subtopic.objects.get(subtopic_name=subtopic, topic_id_id=topic_id)
                        #hashtext = str(current_subtopic.pk) + '-' + str(request.user.pk)
                        #hash_result = hashlib.md5(hashtext.encode())
                        current_subtopic.subtopic_hash = str(uuid.uuid1())#hash_result.hexdigest()
                        current_subtopic.subtopic_url = '-'.join(str(subtopic).lower().split())
                        current_subtopic.save()
                        messages.success(request, 'Topic added with subtopic')
                        i_topic = Topic.objects.get(topic_url=t_id, internship_id__internship_url=i_id)

        context = {
            'form': form,
            'i_topic': i_topic,
            'subtopics': subtopics,
            'rearrange_subtopic': rearrange_subtopic,
        }
        return render(request, 'fossee_math_pages/add-subtopics.html', context)
    else:
        return redirect('dashboard')


@login_required
def delete_assign_topic(request, s_id):
    if request.user.is_staff:
        try:
            subtopic = Subtopic.objects.get(subtopic_hash=s_id)
            subtopic.assigned_user_id = None
            subtopic.save()
            return redirect('assign-topics')
        except:
            return redirect('dashboard')
    else:
        return redirect('dashboard')


@login_required
def add_topics(request):
    if request.user.is_staff:
        form = add_topic()
        topic_order = topicOrder()
        internship = Internship.objects.filter().first()

        if request.method == 'POST':
            if "search_internship" in request.POST:
                internship = Internship.objects.get(pk=request.POST['search_internship'])
            elif "topic_order" in request.POST:
                topoder = request.POST['topic_order']
                topic_id = request.POST['topicid']
                obj = Topic.objects.get(pk=topic_id)
                obj.topic_order = topoder
                obj.save()
            else:
                topic = request.POST['topic']
                id = request.POST['id']
                if topic.strip() == '':
                    messages.error(request, "Fill the field")
                    return redirect(add_topics)
                else:
                    obj = Topic.objects.filter(internship_id_id=id).order_by('topic_order').last()
                    if obj:
                        order = obj.topic_order
                    else:
                        order = 0
                    try:
                        Topic.objects.get(topic_name=topic, internship_id_id=id)
                        messages.error(request, "Topic alredy exists")
                    except:
                        order = order + 1
                        data = Topic(topic_name=topic, internship_id_id=id, topic_order=order)
                        data.save()
                        current_topic = Topic.objects.get(topic_name=topic, internship_id_id=id)
                        current_topic.topic_url = '-'.join(str(topic).lower().split())
                        current_topic.save()
                        messages.success(request, 'Topic added with internship')
                        internship = Internship.objects.get(pk=current_topic.internship_id.pk)

        internship_all = Internship.objects.all()
        topic = Topic.objects.all().order_by('topic_order')

        context = {
            'form': form,
            'internship': internship,
            'internship_all': internship_all,
            'topic': topic,
            'topic_order': topic_order,
        }
        return render(request, 'fossee_math_pages/add-topics.html', context)
    else:
        return redirect('dashboard')


@login_required
def review_submissions(request):
    if request.user.is_staff:
        first_internship = Internship.objects.first()
        first_internship = Internship.objects.get(internship_topic=first_internship)
        interns = User.objects.filter(userdetails__user_role='INTERN')
        internship = Internship.objects.all()
        subtopic = Subtopic.objects.all().order_by('subtopic_order').order_by('topic_id')

        if "search_internship" in request.POST:
            subtopic = Subtopic.objects.filter(topic_id__internship_id_id=request.POST['search_internship']).order_by(
                'subtopic_order').order_by('topic_id')
            first_internship = Internship.objects.get(pk=request.POST['search_internship'])
            interns = Subtopic.objects.filter(topic_id__internship_id_id=request.POST['search_internship'])

        if "search_intern" in request.POST:
            subtopic = Subtopic.objects.filter(assigned_user_id=request.POST['search_intern']).order_by(
                'subtopic_order').order_by('topic_id')

        context = {
            'subtopic': subtopic,
            'internship': internship,
            'first_internship': first_internship,
            'interns': interns,
        }

        return render(request, 'fossee_math_pages/review-submissions.html', context)
    else:
        return redirect('dashboard')


# HERE
@login_required
def manage_interns(request):
    if request.user.is_staff and not request.user.is_superuser:
        form = ManageIntern()
        subtopic = Subtopic.objects.all()
        interns = UserDetails.objects.filter(user_role='INTERN')

        if request.method == 'POST':
            current_user = UserDetails.objects.get(user_id_id=request.POST['assigneduserid'])
            current_user.user_status = request.POST['user_status']
            current_user.save()
            messages.success(request, "Intern Status Changed")

        context = {
            'form': form,
            'interns': interns,
            'subtopic': subtopic,
        }
        return render(request, 'fossee_math_pages/manage-interns.html', context)
    elif request.user.is_superuser:
        interns = UserDetails.objects.filter(user_role="INTERN")
        form = ManageIntern()
        if request.method == 'POST':
            int_id = request.POST["id"]
            obj = UserDetails.objects.get(user_id_id=int_id)
            form = ManageIntern(request.POST or None, instance=obj)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.save()
                messages.success(request, "Changed")
                return redirect('manage-interns')
            else:
                messages.error(request, "Error")
                return redirect('manage-interns')

        context = {
            'interns': interns,
            'form': form,
        }
        return render(request, 'fossee_math_pages/manage-interns.html', context)
    else:
        return redirect('dashboard')


@login_required
def assign_topics(request):
    if request.user.is_staff:
        form = AssignTopic()
        subtopic = Subtopic.objects.all().order_by('topic_id')
        internship = Internship.objects.all()
        first_internsip = Internship.objects.filter(internship_status='ACTIVE').first()

        if request.method == 'POST':
            if "search_internship" in request.POST:
                first_internsip = Internship.objects.get(pk=request.POST['search_internship'])
                try:
                    subtopic = Subtopic.objects.filter(topic_id__internship_id_id=first_internsip.pk)
                except:
                    subtopic = None
            else:
                if request.method == "POST":
                    selectd_subtopic = Subtopic.objects.get(pk=request.POST["subtopicid"])
                    try:
                        user = User.objects.get(pk=request.POST["assigned_user_id"])
                        selectd_subtopic.assigned_user_id_id = user.id
                        selectd_subtopic.save()
                        messages.success(request, 'Intern assigned with topic')
                    except:
                        messages.error(request, "Intern not selected")

        context = {
            'form': form,
            'subtopic': subtopic,
            'intern': internship,
            'chosen_inernship': first_internsip,
        }
        return render(request, 'fossee_math_pages/assign-topics.html', context)
    else:
        return redirect('dashboard')


@login_required
def interns(request):
    if request.user.is_staff:
        topics = Subtopic.objects.all()
        internship_all = Internship.objects.all()
        internship = Internship.objects.first()
        internship = Internship.objects.get(pk=internship.pk)

        if "search_internship" in request.POST:
            internship = Internship.objects.get(pk=request.POST['search_internship'])

        conxext = {
            'topics': topics,
            'internship': internship,
            'internship_all': internship_all,
        }
        return render(request, 'fossee_math_pages/interns.html', conxext)
    else:
        return redirect('dashboard')


@login_required
def internship_progress(request):
    if request.user.is_staff or request.user.is_superuser:
        internship = Internship.objects.first()
        internship = Internship.objects.filter(pk=internship.pk)
        topics = Topic.objects.all()
        subtopics = Subtopic.objects.all()
        internship_all = Internship.objects.all()

        if "search_internship" in request.POST:
            internship = Internship.objects.filter(pk=request.POST['search_internship'])

        context = {
            'internship': internship,
            'topics': topics,
            'subtopics': subtopics,
            'internship_all': internship_all,
            'chosen_internship': internship[0],
        }
        return render(request, 'fossee_math_pages/internship-progress.html', context)

    elif request.user.is_authenticated and not request.user.is_staff and not request.user.is_superuser:
        internship = Internship.objects.all()
        subtopics = Subtopic.objects.all()

        context = {
            'internship': internship,
            'subtopics': subtopics,
        }
        return render(request, 'fossee_math_pages/internship-progress.html', context)

    else:
        return redirect('dashboard')


@login_required
def review_submissions_subtopic(request, s_id):
    if request.user.is_staff:
        subtopic = Subtopic.objects.get(subtopic_hash=s_id)
        data = Data.objects.filter(subtopic_id=subtopic.pk)
        imageformat = ImageFormatting.objects.all()

        if request.method == "POST":
            if "message" in request.POST:
                message = request.POST['message']
                try:
                    obj = Messages.objects.get(subtopic_id_id=subtopic.pk)
                    obj.message = message
                    obj.message_send_date = now()
                    obj.save()
                except:
                    obj = Messages(subtopic_id_id=subtopic.pk, user_id_id=request.user.pk, message=message,
                                   message_send_date=now())
                    obj.save()
            else:
                mentor = request.POST['mentor']
                professor = request.POST['professor']

                try:
                    if mentor.strip() != '' and professor.strip() != "":
                        obj = Contributor.objects.get(subtopic_id_id=subtopic.pk)
                        obj.mentor = mentor
                        obj.professor = professor
                        obj.save()
                except:
                    obj = Contributor(subtopic_id_id=subtopic.pk, contributor=subtopic.assigned_user_id, mentor=mentor,
                                      professor=professor, data_aproval_date=now())
                    obj.save()

        try:
            instance = Messages.objects.get(subtopic_id_id=subtopic.pk)
            form_message = sendMessage(request.POST or None, instance=instance)
        except:
            form_message = sendMessage()

        try:
            instance = Contributor.objects.get(subtopic_id_id=subtopic.pk)
            form = addContributor(request.POST or None, instance=instance)
        except:
            form = addContributor()

        context = {
            'subtopic': subtopic,
            'datas': data,
            'imagesize': imageformat,
            'form': form,
            'form_message': form_message,
        }

        return render(request, 'fossee_math_pages/review-submissions-subtopic.html', context)
    else:
        return redirect('dashboard')


@login_required
def approve_subtopic(request, id):
    if request.user.is_staff:
        instance = Subtopic.objects.get(id=id)
        t_id = instance.pk
        instance.subtopic_status = "ACCEPTED"
        instance.save()
        return redirect('review-submissions-subtopic', instance.subtopic_hash)
    else:
        return redirect('dashboard')


@login_required
def reject_subtopic(request, id):
    if request.user.is_staff:
        instance = Subtopic.objects.get(id=id)
        t_id = instance.pk
        instance.subtopic_status = "REJECTED"
        instance.save()
        return redirect('review-submissions-subtopic', instance.subtopic_hash)
    else:
        return redirect('dashboard')


@login_required
def view_messages(request):
    if not request.user.is_staff and not request.user.is_superuser:
        message = Messages.objects.all()
        context = {
            'message': message
        }
        return render(request, 'fossee_math_pages/messages.html', context)
    else:
        return redirect('dashboard')


@login_required
def user_logout(request):
    logout(request)
    return redirect('index')


def error_404_view(request, exception):
    return render(request, 'fossee_math_pages/404.html')


@login_required
def delete_topic(request, t_id):
    if request.user.is_staff and not request.user.is_superuser:
        try:
            subtopic = Subtopic.objects.filter(topic_id=t_id)
            if subtopic:
                messages.error(request, "Subtopics exist !! delete subtopic firts")
                return redirect('add-topics')
            else:
                topic = Topic.objects.get(pk=t_id)
                topic.delete()
                messages.success(request, "Topic removed !")
                return redirect('add-topics')
        except:
            return redirect('add-topics')

    else:
        return redirect('dashboard')


@login_required
def delete_subtopic(request, t_id, st_id):
    if request.user.is_staff and not request.user.is_superuser:
        subtopic = Subtopic.objects.get(subtopic_hash=st_id)
        try:
            if Data.objects.filter(subtopic_id__topic_id_id=t_id, subtopic_id__subtopic_hash=st_id).exists():
                messages.error(request, "Data exists for this subtopic, cannot delete!!")
                return redirect('add-subtopics', subtopic.topic_id.internship_id.internship_url,
                                subtopic.topic_id.topic_url)
            else:
                subtopic.delete()
                messages.success(request, "Subtopic deleted!")
                return redirect('add-subtopics', subtopic.topic_id.internship_id.internship_url,
                            subtopic.topic_id.topic_url)
        except:
            return redirect('add-subtopics', subtopic.topic_id.internship_id.internship_url,
                            subtopic.topic_id.topic_url)
    else:
        return redirect('dashboard')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        userdetails = UserDetails.objects.get(user_id=user.pk)
        userdetails.user_status = 'ACTIVE'
        userdetails.save()
        return redirect('activate-account')
    else:
        messages.error(request, 'Activation link is invalid!')
        return redirect('login')


def password_set(request):
    form = PasswordChangeForm(user=request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Password Changed Successfully !')
            return redirect(dashboard)

    context = {
        'form': form,
    }
    return render(request, "password_reset/password_set.html", context)
