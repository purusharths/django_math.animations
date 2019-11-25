from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from fossee_math_pages import views
from django.urls import path

urlpatterns = [
    url(r'^login/$',views.login,name='login'),
    path('',views.index, name='index'),
    path('',views.index, name='pagenotfound'),
    path('',views.index, name='content_emplate'),
    path('',views.index, name='internship'),
    path('',views.index, name='real_number_line'),
    path('',views.index, name='realanalysis'),
    path('',views.index, name='topics'),
]
