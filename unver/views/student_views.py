from django.shortcuts import get_object_or_404, render

from .admin_views import login_required_decorator
from ..models import Students, Studentgrades, Attendance


@login_required_decorator
def student_dashboard(request):
    student = get_object_or_404(Students, user=request.user)
    grades = Studentgrades.objects.filter(student=student)
    attendance = Attendance.objects.filter(student=student)

    return render(request, 'dashboard/student.html', {
        "student": student,
        "grades": grades,
        "attendance": attendance
    })
