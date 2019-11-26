from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from fossee_math_pages import views
from django.urls import path

urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    path(r'', views.index, name='index'),
    path(r'', views.index, name='pagenotfound'),
    path(r'', views.index, name='content_emplate'),
    path(r'', views.index, name='internship'),
    path(r'', views.index, name='real_number_line'),
    path(r'', views.index, name='realanalysis'),
    path('topics/', views.topics, name='topics'),
]
