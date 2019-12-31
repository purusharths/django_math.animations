import random

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.shortcuts import get_list_or_404, get_object_or_404
from .forms import AddUserForm1, AddUserForm2, UserLoginForm, AddInternship, ManageInternship, AddIntern
from .models import UserDetails, Internship, Intern
import re
from email_validator import validate_email, EmailNotValidError

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
            data = Internship(internship_topic=internship_topic, internship_thumbnail=internship_thumbnail, internship_status=internship_status)
            data.save()
            messages.success(request, 'Internship added')
            return redirect('admin_add_internship')
        except:
            messages.error(request, 'Some error occured')
            return redirect('admin_add_internship')
    context = {
        'form' : form,
    }
    return render(request,'fossee_math_pages/admin_add_internship.html', context)

@login_required
def admin_add_user(request):
    form = AddUserForm1()
    sub_form = AddUserForm2()
    if request.method == 'POST':
        # register user
        
        firstname = request.POST['first_name']
        lastname = request.POST['last_name']
        email = request.POST['email']
        user_role = request.POST['user_role']
        user_phone = request.POST['user_phone']
        user_status = request.POST['user_status']

        regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]') 
        if User.objects.filter(email=email).exists():
            messages.error(request, 'That email is being used')
            return redirect('admin_add_user')
        if firstname.isdigit():
            messages.error(request, 'Firstname cannot have numbers')
            return redirect('admin_add_user')
        if(regex.search(firstname) == True): 
            messages.error(request, 'Firstname cannot have special characters')
            return redirect('admin_add_user')
        if lastname.isdigit():
            messages.error(request, 'Lastname cannot have numbers')
            return redirect('admin_add_user')
        if(regex.search(lastname) == True): 
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
            user = User.objects.create_user(username=email, email=email, password=password, first_name=firstname,
                                                                        last_name=lastname)
            u_id = User.objects.get(email=email)
            
            print("\n-----+++++",u_id,"\n-------------+++++++++")
            if user_role == 'INTERN':
                addusr = UserDetails(user_id=u_id, user_phone=user_phone, user_role=user_role,
                                                            user_temp_password=password, user_status=user_status)
                addusr.save()
            else:
                addusr = UserDetails(user_id=u_id.id, user_phone=user_phone, user_role=user_role,
                                                            user_temp_password=password, user_status='ACTIVE')
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
        'form' : form,
        'sub_form' :sub_form,
    }
    return render(request, 'fossee_math_pages/admin_add_user.html', context)


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
            messages.success(request,"Changed")
            return redirect('admin_manage_internship') 
        else:
            messages.error(request,"Error")
            return redirect('admin_manage_internship') 
    context = {
            'manage_internships': manage_internships,
            'form' : form
        }
    return render(request,'fossee_math_pages/admin_manage_internship.html',context)

def admin_add_intern(request):
    form = AddIntern()
    internships = Internship.objects.all()
    users = UserDetails.objects.filter(user_role="INTERN", user_status="ACTIVE")
    if request.method == 'POST':
        intern_name = request.POST['user_id']
        topic = request.POST['internship_id']
        temp1 = User.objects.get(id=intern_name)
        temp2 = Internship.objects.get(id=topic)
        if Intern.objects.filter(user_id=intern_name).exists():
            messages.error(request, 'That intern has an internship')
            return redirect('admin_add_intern')
        data = Intern(user_id=temp1, internship_id=temp2)
        data.save()
        messages.success(request, 'Intern added with internship')
        return redirect('admin_add_intern')
       
    context = {
        'internships' : internships,
        'users' : users,
        'form' : form,
    }
    return render(request,'fossee_math_pages/admin_add_intern.html', context)

def admin_view_internship(request):
    data = Intern.objects.all()
    context = {
        'data' : data
    }
    return render(request,'fossee_math_pages/admin_view_internship.html', context)



def dashboard(request):
    return render(request,'fossee_math_pages/dashboard.html')

def home_topics(request):
    return render(request,'fossee_math_pages/home_topics.html')

def home_view_data(request):
    return render(request,'fossee_math_pages/home_view_data.html')

def index(request):
    return render(request,'fossee_math_pages/index.html')

def intern_add_data(request):
    return render(request,'fossee_math_pages/intern_add_data.html')

def intern_view_internship(request):
    return render(request,'fossee_math_pages/intern_view_internship.html')

def intern_edit_data(request):
    return render(request,'fossee_math_pages/intern_edit_data.html')

def intern_view_data(request):
    return render(request,'fossee_math_pages/intern_view_data.html')

def intern_view_topic(request):
    return render(request,'fossee_math_pages/intern_view_topic.html')

def internship(request):
    return render(request,'fossee_math_pages/internship.html')

def user_login(request):
    user = request.user

    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data
            login(request, user)
            # intern_count = 0
            # intern_count = AddUser.objects.filter(role='INTERN').count()
            # staff_count = AddUser.objects.filter(role='STAFF').count()

            # status_active = AddUser.objects.filter(status='ACTIVE').count()
            # status_inactive = AddUser.objects.filter(role='INACTIVE').count()
            # status_suspended = AddUser.objects.filter(role='SUSPENDED').count()
            # context = {
            #     'intern_count': intern_count,
            #     'staff_count': staff_count,
            #     'status_active': status_active,
            #     'status_inactive': status_inactive,
            #     'status_suspended': status_suspended
            # }
            return render(request, "fossee_math_pages/dashboard.html")
        else:
            return render(request, "fossee_math_pages/login.html", {"form": form})
    else:
        form = UserLoginForm()
        return render(request, "fossee_math_pages/login.html", {"form": form})

    
def staff_add_subtopic(request):
    return render(request,'fossee_math_pages/staff_add_subtopic.html')

def staff_add_topics(request):
    return render(request,'fossee_math_pages/staff_add_topics.html')

def staff_aprove_contents(request):
    return render(request,'fossee_math_pages/staff_aprove_contents.html')

def staff_manage_intern(request):
    return render(request,'fossee_math_pages/staff_manage_intern.html')

def staff_view_interns(request):
    return render(request,'fossee_math_pages/staff_view_interns.html')

def staff_view_internship(request):
    return render(request,'fossee_math_pages/staff_view_internship.html')
    
def staff_view_topic(request):
    return render(request,'fossee_math_pages/staff_view_topic.html')

def user_logout(request):
    logout(request)
    return redirect('index')