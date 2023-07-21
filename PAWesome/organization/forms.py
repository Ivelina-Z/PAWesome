from django import forms
from django.forms import FileInput

from PAWesome.animal.models import Animal, AnimalPhotos
from PAWesome.mixins import FormControlMixin
from PAWesome.organization.models import Organization, Employee


class OrganizationForm(FormControlMixin, forms.ModelForm):
    class Meta:
        model = Organization
        exclude = ['email', 'slug', 'user']


class EmployeeForm(FormControlMixin, forms.ModelForm):
    class Meta:
        model = Employee
        exclude = ['email', 'organization', 'user']



