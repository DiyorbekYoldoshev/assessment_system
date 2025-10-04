# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
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
    email = models.EmailField(null=True, blank=True)  # ixtiyoriy
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


class Attendance(models.Model):
    student = models.ForeignKey('Students', models.DO_NOTHING)
    science = models.ForeignKey('Sciences', models.DO_NOTHING)
    date = models.DateField()
    status = models.TextField()

    class Meta:
        managed = False
        db_table = 'Attendance'


class Employees(models.Model):
    user = models.OneToOneField('Users', models.DO_NOTHING)
    position = models.TextField()

    def __str__(self):
        return self.user

    class Meta:
        managed = False
        db_table = 'Employees'


class Faculty(models.Model):
    name = models.TextField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'Faculty'


class Groups(models.Model):
    name = models.TextField()
    faculty = models.ForeignKey(Faculty, models.DO_NOTHING)
    kafedra = models.ForeignKey('Kafedra', models.DO_NOTHING)

    def __str__(self):
        return f"{self.name} - {self.kafedra}"

    class Meta:
        managed = False
        db_table = 'Groups'


class Kafedra(models.Model):
    name = models.TextField()
    faculty = models.ForeignKey(Faculty, models.DO_NOTHING)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'Kafedra'



class Sciences(models.Model):
    name = models.TextField()
    kafedra = models.ForeignKey(Kafedra, models.DO_NOTHING)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'Sciences'


class Semester(models.Model):
    name = models.TextField()
    year = models.IntegerField()

    def __str__(self):
        return f"{self.name} - {self.year}"

    class Meta:
        managed = False
        db_table = 'Semester'


class Studentgrades(models.Model):
    student = models.ForeignKey('Students', models.DO_NOTHING)
    science = models.ForeignKey(Sciences, models.DO_NOTHING)
    semester = models.ForeignKey(Semester, models.DO_NOTHING)
    grade = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'StudentGrades'


class Students(models.Model):
    user = models.OneToOneField('Users', models.DO_NOTHING)
    group = models.ForeignKey(Groups, models.DO_NOTHING)
    admission_year = models.IntegerField()

    def __str__(self):
        return self.user

    class Meta:
        managed = False
        db_table = 'Students'


class Teachersubjects(models.Model):
    teacher = models.ForeignKey('Teachers', models.DO_NOTHING)
    science = models.ForeignKey(Sciences, models.DO_NOTHING)
    semester = models.ForeignKey(Semester, models.DO_NOTHING)

    def __str__(self):
        return self.teacher

    class Meta:
        managed = False
        db_table = 'TeacherSubjects'


class Teachers(models.Model):
    user = models.OneToOneField('Users', models.DO_NOTHING)
    kafedra = models.ForeignKey(Kafedra, models.DO_NOTHING)

    def __str__(self):
        return self.user


    class Meta:
        managed = False
        db_table = 'Teachers'


