from django.shortcuts import render
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout,login,authenticate
from .models import *




def login_required_decorator(funk):
    return login_required(funk,login_url='login_page')


@login_required_decorator
def logout_page(request):
    logout(request)
    return redirect('login_page')

def login_page(request):

    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request=request,username=username,password=password)
        if user is not None:
            login(request, user)
            return redirect('home_page')
    return render(request,'login.html')

@login_required_decorator
def admin_dashboard(request):
    if request.user.role.name != 'Admin':
        return redirect('no-access')
    faculties = Faculty.objects.all()
    kafedras = Kafedra.objects.all()
    groups = Groups.objects.all()
    students = Students.objects.all()
    teachers = Teachers.objects.all()

    ctx = {
        'faculties':faculties,
        'kafdras':kafedras,
        'groups':groups,
        'students':students,
        'teachers':teachers,
    }
    return render(request,'dashboard/admin.html',ctx)


@login_required_decorator
def teacher_dashboard(request):
    if request.user.role.name != 'Teacher':
        return redirect('no-access')

    teacher = Teachers.objects.get(user = request.user)

    teacher_subjects = teacher.teachsersubjects_set.all()

    student_ids = Studentgrades.objects.filter(
        science_id__in=[sub.science.id for sub in teacher_subjects]
    ).values_list("student_id", flat=True).distinct()

    student = Students.objects.filter(id__in=student_ids)

    ctx = {
        'teacher':teacher,
        'teacher_subjects':teacher_subjects,
        'student':student,
    }
    return render(request,'dashboard/teacher.html',ctx)




@login_required_decorator
def student_dashboard(request):
    if request.user.role.name !="Student":
        return redirect('no-access')

    student = Students.objects.get(user = request.user)

    grades = Studentgrades.objects.filter(student=student)
    attendance = Attendance.objects.filter(student=student)

    ctx = {
        'student':student,
        'grades':grades,
        'attendance':attendance,
    }
    return render(request,'dashboard/student.html',ctx)


