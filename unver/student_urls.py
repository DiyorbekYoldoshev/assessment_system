from django.urls import path
from .views.student_views import *


urlpatterns = [
    path('', student_dashboard, name='student_dashboard'),
    path('sciences/', student_sciences, name='student_sciences'),
]