from django import forms
from .models import *



class AdminFrom(forms.ModelForm):

    class Meta:
        pass


class UserRoleForm(forms.ModelForm):
    role = forms.ModelChoiceField(queryset=Roles.objects.all(),required=True)

    class Meta:
        model = Users
        fields = ['role']
