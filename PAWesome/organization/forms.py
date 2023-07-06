from django import forms

from PAWesome.organization.models import Organization


class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        exclude = ['slug']

