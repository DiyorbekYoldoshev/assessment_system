from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from ..forms import UserRoleForm, TeacherForm, FacultyForm, KafedraForm
from ..models import *

# Custom login_required
def login_required_decorator(funk):
    return login_required(funk, login_url='login_page')

# ==================== AUTH ====================
def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request=request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('admin_dashboard')
    return render(request, 'login.html')

@login_required_decorator
def logout_page(request):
    logout(request)
    return redirect('login_page')

# ==================== ADMIN DASHBOARD ====================

def admin_dashboard(request):
    faculties = Faculty.objects.all()
    kafedras = Kafedra.objects.all()
    groups = Groups.objects.all()
    students = Students.objects.all()
    teachers = Teachers.objects.all()

    counts = {
        "faculties": faculties.count(),
        "kafedras": kafedras.count(),
        "groups": groups.count(),
        "students": students.count(),
        "teachers": teachers.count(),
    }

    ctx = {
        'faculties': faculties,
        'kafedras': kafedras,
        'groups': groups,
        'students': students,
        'teachers': teachers,
        'counts': counts,
    }
    return render(request, 'dashboard/admin.html', ctx)

# ==================== USER MANAGEMENT ====================


@login_required_decorator
def admin_faculty_create(request):

    model = Faculty()
    form = FacultyForm(request.POST or None, instance=model)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('faculty_list')
    return render(request,'faculty/form.html',{'form':form})

@login_required_decorator
def admin_faculty_edit(request,pk):

    model = get_object_or_404(Faculty,pk=pk)
    form = FacultyForm(request.POST or None,instance=model)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('faculty_list')
    return render(request,'faculty/form.html',{'model':model,'form':form})

@login_required_decorator
def admin_faculty_delete(request,pk):
    model = get_object_or_404(Faculty,pk=pk)
    model.delete()
    return redirect('faculty_list')


@login_required_decorator
def admin_faculty_list(request):
    faculty = Faculty.objects.all()
    ctx = {
        'faculty': faculty
    }
    return render(request,'faculty/list.html',ctx)
# ==================== KAFEDRA ====================

@login_required_decorator
def admin_kafedra_create(request):
    model = Kafedra()
    form = KafedraForm(request.POST or None, instance=model)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('kafedra_list')
    return render(request, 'kafedra/form.html', {'form': form})

@login_required_decorator
def admin_kafedra_edit(request, pk):
    model = get_object_or_404(Kafedra, pk=pk)
    form = KafedraForm(request.POST or None, instance=model)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('kafedra_list')
    return render(request, 'kafedra/form.html', {'form': form, 'model': model})

@login_required_decorator
def admin_kafedra_delete(request, pk):
    model = get_object_or_404(Kafedra, pk=pk)
    model.delete()
    return redirect('kafedra_list')

@login_required_decorator
def admin_kafedra_list(request):
    kafedras = Kafedra.objects.all()
    ctx = {'kafedras': kafedras}
    return render(request, 'kafedra/list.html', ctx)


@login_required_decorator
def admin_create_user(request):
    model = Users()
    form = UserRoleForm(request.POST or None, instance=model)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('admin_list')
    return render(request, 'admin/form.html', {"form": form})

@login_required_decorator
def admin_edit_user(request, pk):
    model = get_object_or_404(Users, pk=pk)
    form = UserRoleForm(request.POST or None, instance=model)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('admin_list')
    return render(request, 'admin/form.html', {"form": form, "model": model})

@login_required_decorator
def admin_delete_user(request, pk):
    model = get_object_or_404(Users, pk=pk)
    model.delete()
    return redirect('admin_list')

@login_required_decorator
def admin_list_user(request):
    user = Users.objects.all()
    ctx = {'user': user}
    return render(request,'admin/list.html',ctx)

@login_required_decorator
def assign_role(request, user_id):
    user = get_object_or_404(Users, id=user_id)
    if request.method == "POST":
        form = UserRoleForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = UserRoleForm(instance=user)
    return render(request, 'dashboard/assign_role.html', {"form": form, "user": user})

# ==================== TEACHERS ====================
@login_required_decorator
def admin_create_teacher(request):
    model = Teachers()
    form = TeacherForm(request.POST or None, instance=model)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('teacher_list')
    return render(request, 'teacher/form.html', {"form": form})

@login_required_decorator
def admin_edit_teacher(request, pk):
    model = get_object_or_404(Teachers, pk=pk)
    form = TeacherForm(request.POST or None, instance=model)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('teacher_list')
    return render(request, 'teacher/form.html', {"form": form, "model": model})

@login_required_decorator
def admin_delete_teacher(request, pk):
    model = get_object_or_404(Teachers, pk=pk)
    model.delete()
    return redirect('teacher_list')

@login_required_decorator
def admin_list_teacher(request):
    teachers = Teachers.objects.select_related('user', 'kafedra')
    return render(request, 'teacher/list.html', {'teachers': teachers})

# ==================== DASHBOARDS ====================

