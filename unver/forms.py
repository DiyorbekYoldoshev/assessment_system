from django import forms
from .models import *


class FacultyForm(forms.ModelForm):
    class Meta:
        model = Faculty
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter faculty name...'})
        }
class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teachers
        fields = '__all__'
        widgets = {
            'user': forms.Select(attrs={'class':'form-control'}),
            'kafedra': forms.Select(attrs={'class':'form-control'}),
        }

class KafedraForm(forms.ModelForm):
    class Meta:
        model = Kafedra
        fields = "__all__"
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'faculty': forms.Select(attrs={'class':'form-control'})
        }
class UserRoleForm(forms.ModelForm):
    role = forms.ModelChoiceField(queryset=Roles.objects.all(), required=True)

    class Meta:
        model = Users
        fields = ['role']



class UserForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}),
        required=False
    )

    class Meta:
        model = Users
        fields = ['username', 'full_name', 'email', 'role', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter full name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user

class StudentForm(forms.ModelForm):
    class Meta:
        model = Students
        fields = "__all__"
        widgets = {
            'user': forms.Select(attrs={'class':'form-control'}),
            'group':forms.Select(attrs={'class':'form-control'}),
            'admission_year':forms.NumberInput(attrs={'class':'form-control'}),
        }

class GroupForm(forms.ModelForm):
    class Meta:
        model = Groups
        fields = "__all__"
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'faculty': forms.Select(attrs={'class':'form-control'}),
            'kafedra': forms.Select(attrs={'class':'form-control'})
        }
