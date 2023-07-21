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


class AnimalForm(FormControlMixin, forms.ModelForm):
    formset = None

    class Meta:
        model = Animal
        exclude = ['date_of_publication', 'organization', 'slug']
        widgets = {
            'location': forms.HiddenInput()
        }


class AnimalPhotoForm(FormControlMixin, forms.ModelForm):
    photo = forms.ImageField(widget=FileInput)

    class Meta:
        model = AnimalPhotos
        fields = '__all__'
