from django import forms
from django.contrib.gis import forms as gis_form
from PAWesome.animal.models import Animal
from PAWesome.organization.models import Organization
from leaflet.forms.widgets import LeafletWidget


class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        exclude = ['slug']


# class MapWidget(LeafletWidget):
#     template_name = 'map.html'


class AnimalFrom(forms.ModelForm):
    class Meta:
        model = Animal
        exclude = ['date_of_publication', 'organization']
        widgets = {
            'location': forms.HiddenInput()
        }
