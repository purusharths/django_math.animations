from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('internship/', views.internship, name='internship'),
    path('topics/', views.topics, name='topics'),
<<<<<<< HEAD
    path('topic_details/',views.topic_details,name='topic_details'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('manage_intern/',views.manage_intern,name='manage_intern'),
    path('aprove_contents/',views.aprove_contents,name='aprove_contents'),
    path('manage_intern/',views.manage_intern,name='manage_intern'),
    path('add_details/',views.add_details,name='add_details'),
    path('view_details/',views.view_details,name='view_details'),
    path('view_data/<int:view_id>',views.view_data,name="view_data"),
    path('edit_data/',views.edit_data,name='edit_data'),
    path('edit_data/<int:edit_id>',views.edit_data,name="edit_data"),
    path('add_user/',views.add_user,name='add_user'),
=======
    path('dashboard/', views.dashboard, name='dashboard'),
    path('manage_intern/', views.manage_intern, name='manage_intern'),
    path('aprove_contents/', views.aprove_contents, name='aprove_contents'),
    path('manage_intern/', views.manage_intern, name='manage_intern'),
    path('add_details/', views.add_details, name='add_details'),
    path('view_details/', views.view_details, name='view_details'),
    path('view_data/<int:view_id>', views.view_data, name="view_data"),
    path('viewdata/<int:view_id>', views.viewdata, name="viewdata"),
    path('edit_data/', views.edit_data, name='edit_data'),
    path('add_user/', views.add_user, name='add_user'),
>>>>>>> b2f8c8160764fa57850a5d2a5b562860f2a1259a
]
