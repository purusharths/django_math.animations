from django.conf.urls.static import static
from django.urls import path

from FOSSEE_math import settings
from . import views

urlpatterns = [
                  path('admin_view_intern/<int:id>', views.admin_view_intern, name='admin_view_intern'),
                  path('admin_add_intern/', views.admin_add_intern, name='admin_add_intern'),
                  path('staff_delete_data/<str:id>', views.staff_delete_data, name='staff_delete_data'),
                  path('staff_aprove_subtopic/<int:id>', views.staff_aprove_subtopic, name='staff_aprove_subtopic'),
                  path('staff_reject_subtopic/<int:id>', views.staff_reject_subtopic, name='staff_reject_subtopic'),
                  path('intern_delete_data/<str:id>', views.intern_delete_data, name='intern_delete_data'),
                  path('intern_update_media/<str:id>', views.intern_update_media, name='intern_update_media'),


                  # CHANGED
                  path('dashboard/messages/', views.view_messages, name='messages'),
                  path('dashboard/add-internship/', views.add_internship, name='add-internship'),
                  path('dashboard/add-users/', views.add_users, name='add-users'),
                  path('dashboard/add-topics/', views.add_topics, name='add-topics'),
                  path('dashboard/add-subtopics/<str:i_id>/<str:t_id>', views.add_subtopics, name='add-subtopics'),
                  path('dashboard/add-submission/', views.add_submission, name='add-submission'),
                  path('dashboard/add-submission/<str:st_id>', views.add_submission_subtopic,
                       name='add-submission-subtopic'),
                  path('dashboard/add-submisson/<str:t_id>/edit-image/<str:id>', views.edit_image, name='edit-image'),
                  path('dashboard/add-submisson/<str:t_id>/edit-text/<str:id>', views.edit_text, name='edit-text'),
                  path('dashboard/assign-topics', views.assign_topics, name='assign-topics'),
                  path('dashboard/interns/', views.interns, name='interns'),
                  path('dashboard/internship-progress/', views.internship_progress, name='internship-progress'),
                  path('dashboard/manage-interns/', views.manage_interns, name='manage-interns'),
                  path('dashboard/manage-internship/', views.manage_internship, name='manage-internship'),
                  path('dashboard/review-submissions/', views.review_submissions, name='review-submissions'),
                  path('dashboard/review-submissions/<str:s_id>', views.review_submissions_subtopic,
                       name='review-submissions-subtopic'),
                  path('dashboard/review-submissons/<str:t_id>/edit-image/<str:id>', views.edit_image, name='edit-image-staff'),
                  path('dashboard/review-submissons/<str:t_id>/edit-text/<str:id>', views.edit_text, name='edit-text-staff'),
                  ##

                  # ALREADY OKAY
                  path('', views.index, name='index'),
                  path('contents/<str:internship>', views.contents, name='contents'),
                  path('contents/<str:internship>/<str:topic>/<str:subtopic>', views.home_details, name='home_details'),
                  path('dashboard/', views.dashboard, name='dashboard'),
                  path('internship/', views.internship, name='internship'),
                  path('login/', views.user_login, name='login'),
                  path('logout/', views.user_logout, name='logout'),
                  ##
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
