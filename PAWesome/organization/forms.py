from django import forms
from PAWesome.animal.models import Animal, AnimalPhotos
from PAWesome.organization.models import Organization


class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        exclude = ['slug']


class AnimalForm(forms.ModelForm):
    class Meta:
        model = Animal
        exclude = ['date_of_publication', 'organization', 'slug']
        widgets = {
            'location': forms.HiddenInput()
        }
