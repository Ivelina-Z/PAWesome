from django import forms
from django.contrib.gis import forms as gis_form
from PAWesome.animal.models import Animal
from PAWesome.organization.models import Organization


class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        exclude = ['slug']


class AnimalFrom(gis_form.Form):
    point = gis_form.PointField(widget=gis_form.OSMWidget(attrs={"display_raw": True}))

    # class Meta:
    #     model = Animal
    #     exclude = ['date_of_publication']
