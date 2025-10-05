from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class Roles(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Roles'
        managed = True

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, full_name=None, role=None):
        if not username:
            raise ValueError("Username bo'lishi shart")
        user = self.model(username=username, full_name=full_name, role=role)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, full_name="Admin"):
        user = self.create_user(username=username, password=password, full_name=full_name)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Users(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(null=True, blank=True)
    role = models.ForeignKey('Roles', on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['full_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'Users'
        managed = True

class Faculty(models.Model):
    name = models.TextField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        db_table = 'Faculty'

class Kafedra(models.Model):
    name = models.TextField()
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        db_table = 'Kafedra'

class Groups(models.Model):
    name = models.TextField()
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    kafedra = models.ForeignKey('Kafedra', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.kafedra}"

    class Meta:
        managed = True
        db_table = 'Groups'

class Sciences(models.Model):
    name = models.TextField()
    kafedra = models.ForeignKey(Kafedra, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        db_table = 'Sciences'

class Semester(models.Model):
    name = models.TextField()
    year = models.IntegerField()

    def __str__(self):
        return f"{self.name} - {self.year}"

    class Meta:
        managed = True
        db_table = 'Semester'

class Employees(models.Model):
    user = models.OneToOneField('Users', on_delete=models.CASCADE)
    position = models.TextField()

    def __str__(self):
        return str(self.user.username)

    class Meta:
        managed = True
        db_table = 'Employees'

class Teachers(models.Model):
    user = models.OneToOneField('Users', on_delete=models.CASCADE)
    kafedra = models.ForeignKey(Kafedra, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user.username)

    class Meta:
        managed = True
        db_table = 'Teachers'

class Students(models.Model):
    user = models.OneToOneField('Users', on_delete=models.CASCADE)
    group = models.ForeignKey(Groups, on_delete=models.CASCADE)
    admission_year = models.IntegerField()

    def __str__(self):
        return str(self.user.username)

    class Meta:
        managed = True
        db_table = 'Students'

class Teachersubjects(models.Model):
    teacher = models.ForeignKey('Teachers', on_delete=models.CASCADE)
    science = models.ForeignKey(Sciences, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.teacher.user.full_name} - {self.science.name}"

    class Meta:
        managed = True
        db_table = 'TeacherSubjects'

class Studentgrades(models.Model):
    student = models.ForeignKey('Students', on_delete=models.CASCADE)
    science = models.ForeignKey(Sciences, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    grade = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'StudentGrades'

class Attendance(models.Model):
    student = models.ForeignKey('Students', on_delete=models.CASCADE)
    science = models.ForeignKey('Sciences', on_delete=models.CASCADE)
    date = models.DateField()
    status = models.TextField()

    class Meta:
        managed = True
        db_table = 'Attendance'
