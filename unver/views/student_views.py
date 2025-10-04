from django.shortcuts import render
from ..models import Users, Students, Studentgrades, Attendance
from .admin_views import login_required_decorator

@login_required_decorator
def student_dashboard(request):
    # Sessiyadan foydalanuvchi id sini olish
    user_id = request.session.get('user_id')

    if not user_id:
        return render(request, 'error.html', {"msg": "Foydalanuvchi tizimga kirmagan."})

    try:
        user = Users.objects.get(id=user_id)
    except Users.DoesNotExist:
        return render(request, 'error.html', {"msg": "Users jadvalidan foydalanuvchi topilmadi."})

    # Students jadvalidan foydalanuvchi asosida izlash
    try:
        student = Students.objects.get(user=user)
    except Students.DoesNotExist:
        return render(request, 'student/no_student.html', {"user": user})

    grades = Studentgrades.objects.filter(student=student)
    attendance = Attendance.objects.filter(student=student)

    return render(request, 'student/student_dashboard.html', {
        "student": student,
        "grades": grades,
        "attendance": attendance
    })
