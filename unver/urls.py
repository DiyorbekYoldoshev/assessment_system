from django.urls import path
from .views import *

urlpatterns = [
    # Auth
    path('login/', login_page, name='login_page'),
    path('logout/', logout_page, name='logout_page'),

    # Dashboard
    path('', admin_dashboard, name='admin_dashboard'),
    path('teacher/', teacher_dashboard, name='teacher_dashboard'),

    # Faculties
    path('faculty/create/',admin_faculty_create,name='faculty_create'),
    path('faculty/<int:pk>/edit/',admin_faculty_edit,name='faculty_edit'),
    path('faculty/<int:pk>/delete/',admin_faculty_delete,name='faculty_delete'),
    path('faculty/list/',admin_faculty_list,name='faculty_list'),

    # Kafedra
    path('kafedra/create/', admin_kafedra_create, name='kafedra_create'),
    path('kafedra/<int:pk>/edit/', admin_kafedra_edit, name='kafedra_edit'),
    path('kafedra/<int:pk>/delete/', admin_kafedra_delete, name='kafedra_delete'),
    path('kafedra/list/', admin_kafedra_list, name='kafedra_list'),

    # User management
    path('user/list/', admin_list_user, name='admin_list'),
    path('user/create/', admin_create_user, name='admin_create'),
    path('user/<int:pk>/edit/', admin_edit_user, name='admin_edit'),
    path('user/<int:pk>/delete/', admin_delete_user, name='admin_delete'),
    # Teachers
    path('teacher/create/', admin_create_teacher, name='teacher_create'),
    path('teacher/<int:pk>/edit/', admin_edit_teacher, name='teacher_edit'),
    path('teacher/<int:pk>/delete/', admin_delete_teacher, name='teacher_delete'),
    path('teacher/list/', admin_list_teacher, name='teacher_list'),

    # core
    path('assign-role/<int:user_id>/', assign_role, name='assign_role'),
]

