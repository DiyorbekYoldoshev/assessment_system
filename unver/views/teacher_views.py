from django.shortcuts import get_object_or_404, render
from ..models import Teachers, Studentgrades, Students, Users
from .admin_views import login_required_decorator


# @role_required(['teacher'])
def teacher_dashboard(request):
    user_id = request.session.get('user_id')
    user = get_object_or_404(Users, id=user_id)
    teacher = get_object_or_404(Teachers, user=user)

    teacher_subjects = teacher.teachersubjects_set.all()
    student_ids = Studentgrades.objects.filter(
        science_id__in=[sub.science.id for sub in teacher_subjects]
    ).values_list("student_id", flat=True).distinct()

    students = Students.objects.filter(id__in=student_ids)

    return render(request, 'dashboard/teacher.html', {
        "teacher": teacher,
        "teacher_subjects": teacher_subjects,
        "students": students
    })
