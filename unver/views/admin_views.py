from functools import wraps

from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import check_password
from ..models import *
from ..forms import UserRoleForm, TeacherForm, FacultyForm, KafedraForm, AdminForm


# def login_required_decorator(view_func):
#     @wraps(view_func)
#     def _wrapped(request, *args, **kwargs):
#         user_id = request.session.get('user_id')
#         if not user_id:
#             return redirect('login_page')
#
#         user = Users.objects.filter(pk=user_id).first()
#         if not user:
#             request.session.flush()
#             return redirect('login_page')
#
#         request.current_user = user
#         return view_func(request, *args, **kwargs)
#
#     return _wrapped
#
#
# def role_required(allowed_roles):
#     def decorator(view_func):
#         @wraps(view_func)
#         def _wrapped(request, *args, **kwargs):
#             user_id = request.session.get('user_id')
#             if not user_id:
#                 return redirect('login_page')
#
#             user = Users.objects.filter(pk=user_id).first()
#             if not user:
#                 request.session.flush()
#                 return redirect('login_page')
#
#             role = request.session.get('role', '')
#             if role not in allowed_roles:
#                 return render(request, 'error.html', {'msg': 'Sizda ruxsat yo\'q!'})
#
#             request.current_user = user
#             return view_func(request, *args, **kwargs)
#
#         return _wrapped
#
#     return decorator
#
#
# # ==================== AUTH ====================
# def login_page(request):
#     if request.method == "POST":
#         username = request.POST.get('username', '').strip()
#         password = request.POST.get('password', '')
#
#         print(f"Login attempt: username={username}, password={password}")  # DEBUG
#
#         user = Users.objects.filter(username=username).first()
#         print(f"User found: {user}")  # DEBUG
#
#         if user:
#             print(f"Stored password hash: {user.password}")  # DEBUG
#             print(f"Password check result: {check_password(password, user.password)}")  # DEBUG
#
#             if check_password(password, user.password):
#                 request.session['user_id'] = user.id
#                 request.session['role'] = user.role.name.lower() if user.role and user.role.name else ''
#
#                 role = request.session['role']
#                 print(f"User role: {role}")  # DEBUG
#
#                 if role == 'admin':
#                     return redirect('admin_dashboard')
#                 elif role == 'teacher':
#                     return redirect('teacher_dashboard')
#                 elif role == 'student':
#                     return redirect('student_dashboard')
#                 else:
#                     return redirect('login_page')
#
#         return render(request, 'login.html', {
#             'error': 'Username yoki parol noto\'g\'ri',
#             'username': username
#         })
#
#     return render(request, 'login.html')
#
# @login_required_decorator
# def logout_page(request):
#     request.session.flush()
#     return redirect('login_page')
def login_required_decorator(func):
    return login_required(func, login_url='login_page')


@login_required_decorator
def logout_page(request):
    logout(request)
    return redirect("login_page")


def login_page(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, password=password, username=username)
        if user is not None:
            login(request, user)
            return redirect("admin_list")

    return render(request, 'login.html')

# ==================== ADMIN DASHBOARD ====================
# @role_required(['admin'])
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


# ==================== FACULTY ====================
# @role_required(['admin'])
def admin_faculty_create(request):
    model = Faculty()
    form = FacultyForm(request.POST or None, instance=model)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('faculty_list')
    return render(request, 'faculty/form.html', {'form': form})


# @role_required(['admin'])
def admin_faculty_edit(request, pk):
    model = get_object_or_404(Faculty, pk=pk)
    form = FacultyForm(request.POST or None, instance=model)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('faculty_list')
    return render(request, 'faculty/form.html', {'model': model, 'form': form})


# @role_required(['admin'])
def admin_faculty_delete(request, pk):
    model = get_object_or_404(Faculty, pk=pk)
    model.delete()
    return redirect('faculty_list')


# @role_required(['admin'])
def admin_faculty_list(request):
    faculty = Faculty.objects.all()
    ctx = {'faculty': faculty}
    return render(request, 'faculty/list.html', ctx)


# ==================== KAFEDRA ====================
# @role_required(['admin'])
def admin_kafedra_create(request):
    model = Kafedra()
    form = KafedraForm(request.POST or None, instance=model)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('kafedra_list')
    return render(request, 'kafedra/form.html', {'form': form})


# @role_required(['admin'])
def admin_kafedra_edit(request, pk):
    model = get_object_or_404(Kafedra, pk=pk)
    form = KafedraForm(request.POST or None, instance=model)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('kafedra_list')
    return render(request, 'kafedra/form.html', {'form': form, 'model': model})


# @role_required(['admin'])
def admin_kafedra_delete(request, pk):
    model = get_object_or_404(Kafedra, pk=pk)
    model.delete()
    return redirect('kafedra_list')


# @role_required(['admin'])
def admin_kafedra_list(request):
    kafedras = Kafedra.objects.all()
    ctx = {'kafedras': kafedras}
    return render(request, 'kafedra/list.html', ctx)


# ==================== USER MANAGEMENT ====================
# @role_required(['admin'])
def admin_create_user(request):
    model = Users()
    form = AdminForm(request.POST or None, instance=model)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('admin_list')
    return render(request, 'admin/form.html', {"form": form})


# @role_required(['admin'])
def admin_edit_user(request, pk):
    model = get_object_or_404(Users, pk=pk)
    form = AdminForm(request.POST or None, instance=model)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('admin_list')
    return render(request, 'admin/form.html', {"form": form, "model": model})


# @role_required(['admin'])
def admin_delete_user(request, pk):
    model = get_object_or_404(Users, pk=pk)
    model.delete()
    return redirect('admin_list')


# @role_required(['admin'])
def admin_list_user(request):
    user = Users.objects.all()
    ctx = {'user': user}
    return render(request, 'admin/list.html', ctx)


# @role_required(['admin'])
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
# @role_required(['admin'])
def admin_create_teacher(request):
    model = Teachers()
    form = TeacherForm(request.POST or None, instance=model)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('teacher_list')
    return render(request, 'teacher/form.html', {"form": form})


# @role_required(['admin'])
def admin_edit_teacher(request, pk):
    model = get_object_or_404(Teachers, pk=pk)
    form = TeacherForm(request.POST or None, instance=model)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('teacher_list')
    return render(request, 'teacher/form.html', {"form": form, "model": model})


# @role_required(['admin'])
def admin_delete_teacher(request, pk):
    model = get_object_or_404(Teachers, pk=pk)
    model.delete()
    return redirect('teacher_list')


# @role_required(['admin'])
def admin_list_teacher(request):
    teachers = Teachers.objects.select_related('user', 'kafedra')
    return render(request, 'teacher/list.html', {'teachers': teachers})

