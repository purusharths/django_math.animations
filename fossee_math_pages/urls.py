from django.conf.urls.static import static
from django.urls import path

from FOSSEE_math import settings
from . import views

urlpatterns = [
                  path('', views.index, name='index'),
                  path('admin_add_internship/', views.admin_add_internship, name='admin_add_internship'),
                  path('admin_minternshipanage_internship/', views.admin_manage_internship, name='admin_manage_internship'),
                  path('admin_view_intern/<int:id>', views.admin_view_intern, name='admin_view_intern'),
                  path('admin_add_intern/', views.admin_add_intern, name='admin_add_intern'),
                  path('admin_view_users/', views.admin_view_users, name='admin_view_users'),
                  path('admin_manage_intern/', views.admin_manage_intern, name='admin_manage_intern'),
                  path('admin_view_intership/', views.admin_view_intership, name='admin_view_internshp'),
                  path('dashboard/', views.dashboard, name='dashboard'),
                  path('contents/<str:internship>', views.home_view_data, name='contents'),
                  path('contents/<str:internship>/<str:topic>/<str:subtopic>', views.home_details, name='home_details'),
                  ## CHANGING
                  path('add-submission/<str:st_id>', views.add_submission_intern, name='add-submission-intern'),
                  path('intern_update_data/<int:id>', views.intern_update_data, name='intern_update_data'),
                  path('intern_update_media/<int:id>', views.intern_update_media, name='intern_update_media'),
                  path('intern_delete_data/<str:id>', views.intern_delete_data, name='intern_delete_data'),
                  path('intern_view_internship/', views.intern_view_internship, name='intern_view_internship'),
                  # CHANGING
                  path('add-submission/', views.add_submission , name='add-submission'),
                  ##
                  path('intern_update_image_size/<int:id>', views.intern_update_image_size,
                       name='intern_update_image_size'),
                  path('internship/', views.internship, name='internship'),
                  path('login/', views.user_login, name='login'),
                  #CHANGING
                  path('add-subtopics/<int:id>', views.add_subtopics, name='add-subtopics'),
                  ##
                  # CHANGING
                  path('add-topics/', views.add_topics, name='add-topics'),
                  ##
                  path('staff_aprove_contents/', views.staff_aprove_contents, name='staff_aprove_contents'),
                  path('staff_manage_intern/', views.staff_manage_intern, name='staff_manage_intern'),
                  # CHANGING
                  path('interns/', views.interns, name='interns'),
                  ##
                  path('staff_view_internship/', views.staff_view_internship, name='staff_view_internship'),
                  path('staff_view_topic/<int:s_id>', views.staff_view_topic, name='staff_view_topic'),
                  # CHANGING
                  path('assign-topics', views.assign_topics, name='assign-topics'),
                  ##
                  path('staff_update_data/<int:id>', views.staff_update_data, name='staff_update_data'),
                  path('staff_delete_data/<int:id>', views.staff_delete_data, name='staff_delete_data'),
                  path('staff_aprove_subtopic/<int:id>', views.staff_aprove_subtopic, name='staff_aprove_subtopic'),
                  path('staff_reject_subtopic/<int:id>', views.staff_reject_subtopic, name='staff_reject_subtopic'),
                  path('staff_add_contribution/<int:id>', views.staff_add_contribution, name='staff_add_contribution'),
                  path('staff_update_image_size/<int:id>', views.staff_update_image_size,
                       name='staff_update_image_size'),
                  path('logout/', views.user_logout, name='logout'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
