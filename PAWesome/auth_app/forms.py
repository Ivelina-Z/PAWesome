from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.utils.text import slugify
from phonenumber_field.formfields import PhoneNumberField

from PAWesome.mixins import FormControlMixin
from PAWesome.organization.models import Organization, Employee

UserModel = get_user_model()


class OrganizationRegistrationForm(FormControlMixin, UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Name'

    email = forms.EmailField()
    phone_number = PhoneNumberField()

    class Meta(UserCreationForm.Meta):
        model = UserModel
        fields = ('email', 'username', 'phone_number', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)

        if commit:
            user.is_staff = True
            user.is_active = False
            user.save()
            user.groups.add(Group.objects.get(name='Organizations'))
            organization = Organization.objects.create(
                name=self.cleaned_data['username'],
                phone_number=self.cleaned_data['phone_number'],
                email=self.cleaned_data['email'],
                slug=slugify(self.cleaned_data['username']),
                user=user
            )
            organization.save()

        return user


class EmployeeRegistrationForm(FormControlMixin, UserCreationForm):
    def __init__(self, *args, **kwargs):
        self.request_user = kwargs.pop('request_user')
        super().__init__(*args, **kwargs)

    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    phone_number = PhoneNumberField()

    class Meta(UserCreationForm.Meta):
        model = UserModel
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)

        if commit:
            user.username = self.cleaned_data['email']
            user.is_active = False
            user.save()
            user.groups.add(Group.objects.get(name='Employees'))
            employee = Employee.objects.create(
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                email=self.cleaned_data['email'],
                phone_number=self.cleaned_data['phone_number'],
                organization=self.request_user.organization,
                user=user
            )
            employee.save()
        return user
