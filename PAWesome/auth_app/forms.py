from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, PasswordResetForm, \
    SetPasswordForm
from django.contrib.auth.models import Group
from django.utils.text import slugify
from phonenumber_field.formfields import PhoneNumberField

from PAWesome.mixins import FormControlMixin
from PAWesome.organization.models import Organization, Employee

UserModel = get_user_model()


class OrganizationRegistrationForm(FormControlMixin, UserCreationForm):
    name = forms.CharField(max_length=50)
    email = forms.EmailField()
    phone_number = PhoneNumberField()

    class Meta(UserCreationForm.Meta):
        model = UserModel
        fields = ('email', 'name', 'phone_number', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)

        if commit:
            user.username = self.cleaned_data['email']
            user.is_staff = True
            user.is_active = False
            user.save()
            user.groups.add(Group.objects.get(name='Organizations'))
            organization = Organization.objects.create(
                name=self.cleaned_data['name'],
                phone_number=self.cleaned_data['phone_number'],
                email=self.cleaned_data['email'],
                slug=slugify(self.cleaned_data['name']),
                user=user
            )
            organization.save()

        return user


class EmployeeRegistrationForm(FormControlMixin, UserCreationForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    phone_number = PhoneNumberField()

    class Meta(UserCreationForm.Meta):
        model = UserModel
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'password1', 'password2')


class LoginForm(FormControlMixin, AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['placeholder'] = field_name.capitalize() if field_name != 'username' else 'Email'
            self.fields[field_name].label = ''
            self.fields[field_name].widget.attrs['class'] = 'form-control'


class CustomPasswordChangeForm(FormControlMixin, PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        new_field_label = ['Стара парола', 'Нова парола', 'Потвърждение на нова парола']
        for field_name, field_label in zip(self.fields, new_field_label):
            self.fields[field_name].label = field_label


class CustomPasswordResetForm(FormControlMixin, PasswordResetForm):
    pass


class CustomPasswordConfirmForm(FormControlMixin, SetPasswordForm):
    pass
