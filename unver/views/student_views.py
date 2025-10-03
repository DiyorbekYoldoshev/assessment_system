from django.shortcuts import get_object_or_404, render

from .admin_views import login_required_decorator
from ..models import Students, Studentgrades, Attendance


@login_required_decorator
def student_dashboard(request):
    try:
        student = Students.objects.get(user=request.user)
    except Students.DoesNotExist:
        return render(request, "student/no_student.html")

    grades = Studentgrades.objects.filter(student=student)
    attendance = Attendance.objects.filter(student=student)

    return render(request, "student/student_dashboard.html", {
        "student": student,
        "grades": grades,
        "attendance": attendance
    })

def student_list(request):
    pass

