from django import forms
from .models import *


class FacultyForm(forms.ModelForm):
    class Meta:
        model = Faculty
        fields = "__all__"
        widgets = {
            'faculty': forms.Select(attrs={'class':'form-control'})
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
        # fields = ['role']
        fields = "__all__"
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'})
        }

class AdminForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = "__all__"
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'})
        }