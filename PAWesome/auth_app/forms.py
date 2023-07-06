from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.text import slugify
from phonenumber_field.formfields import PhoneNumberField

from PAWesome.organization.models import Organization


class RegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Name'

    email = forms.EmailField()
    phone_number = PhoneNumberField()

    class Meta(UserCreationForm.Meta):
        fields = ('email', 'username', 'phone_number', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)

        if commit:
            user.save()
            organization = Organization.objects.create(
                name=self.cleaned_data['username'],
                phone_number=self.cleaned_data['phone_number'],
                email=self.cleaned_data['email'],
                slug=slugify(self.cleaned_data['username']),
                user=user
            )
            organization.save()
        return user
