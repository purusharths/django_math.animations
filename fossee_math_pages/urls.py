from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from fossee_math_pages import views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('logout/',views.user_logout,name='logout'),
    path('internship/', views.internship, name='internship'),
    path('topics/', views.topics, name='topics'),
    path('topic_details/',views.topic_details,name='topic_details'),
    path('dashboard/',views.dashboard,name='dashboard'),
<<<<<<< HEAD
    path('add_intern/', views.add_intern, name='add_intern'),

    path('', views.index, name='real_number_line'),
    path('', views.index, name='realanalysis'),
    path('', views.index, name='pagenotfound'),
    path('', views.index, name='content_emplate'),
    # path('', views.InternForm),
=======
    path('manage_intern/',views.manage_intern,name='manage_intern'),
    path('aprove_contents/',views.aprove_contents,name='aprove_contents'),
    path('manage_intern/',views.manage_intern,name='manage_intern'),
    path('add_details/',views.add_details,name='add_details'),
    path('view_details/',views.view_details,name='view_details'),
>>>>>>> 3481a84c5d36113b3a74817f2fc91d921ba2643e
]
