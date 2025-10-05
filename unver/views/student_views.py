from django.shortcuts import render
from ..models import Users, Students, Studentgrades, Attendance, Sciences
from .admin_views import login_required_decorator


# @role_required(['student'])
def student_dashboard(request):
    user_id = request.session.get('user_id')

    try:
        user = Users.objects.all()
        # user = Users.objects.get(id=user_id)
        student = Students.objects.all()
        # student = Students.objects.get(user=user)
    except Users.DoesNotExist:
        return render(request, 'error.html', {"msg": "Foydalanuvchi topilmadi."})
    except Students.DoesNotExist:
        return render(request, 'student/no_student.html', {"user": user})

    # grades = Studentgrades.objects.filter(student=student)
    grades = Studentgrades.objects.all()
    # attendance = Attendance.objects.filter(student=student)
    attendance = Attendance.objects.all()

    return render(request, 'student/student_dashboard.html', {
        "student": student,
        "grades": grades,
        "attendance": attendance
    })


def student_sciences(request):
    sciences = Sciences.objects.all()

    ctx = {
        'sciences':sciences
    }
    return render(request,'student/sciences.html',ctx)






