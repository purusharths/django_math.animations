"""FOSSEE_math URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path

import fossee_math_pages.views as myview

urlpatterns = [
    path('', include('fossee_math_pages.urls')),
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),

    path('password_reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='password_reset/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password_reset/',
         auth_views.PasswordResetView.as_view(template_name='password_reset/password_reset_form.html'),
         name='password_reset'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_complete.html'),
         name='password_reset_complete'),
    path('activate/<uidb64>/<token>/',
         myview.activate, name='activate'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'fossee_math_pages.views.error_404_view'
handler500 = 'fossee_math_pages.views.error_500_view'
