from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from fossee_math_pages import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$',views.login,name='login'),
]
