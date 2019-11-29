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

    path('', views.index, name='real_number_line'),
    path('', views.index, name='realanalysis'),
    path('', views.index, name='pagenotfound'),
    path('', views.index, name='content_emplate'),
    path('', views.InternForm),
]
