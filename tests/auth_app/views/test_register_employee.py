from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase, Client
from django.urls import reverse

from PAWesome.organization.models import Employee
from tests.setup import _create_user_with_organization_profile


class TestRegisterEmployee(TestCase):
    def setUp(self):
        self.user, self.organization, self.group = _create_user_with_organization_profile(
            ['add_employee', 'add_customuser']
        )
        self.user_model = get_user_model()
        self.url = reverse('organization-register-employee')

        self.employee_group = Group.objects.create(name='Employees')

        self.employee_data = {
            'first_name': 'Test First Name',
            'last_name': 'Test Last Name',
            'email': 'test@mail.com',
            'phone_number': '0894001122',
            'password1': 'testpass',
            'password2': 'testpass'
        }
        self.client = Client()

    def test__register_employee_no_permissions__should_return_forbidden(self):
        self.user.groups.remove(self.group)
        self.client.force_login(self.user)

        response = self.client.post(self.url)

        self.assertEquals(response.status_code, 403)

    def test__register_employee_not_authenticated__should_redirect_to_login(self):
        response = self.client.post(self.url)
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('login') + f'?next={self.url}')

    def test__register_employee_valid_form__should_create_user_employee_profile_and_send_mail(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url, data=self.employee_data)

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('homepage'))

        new_user = self.user_model.objects.get(email=self.employee_data['email'])
        new_employee_profile = Employee.objects.get(user=new_user.pk)
        new_employee_field_values = {k: v for k, v in new_employee_profile.__dict__.items() if k != '_state'}
        for field_name, field_value in new_employee_field_values.items():
            if field_name in self.employee_data:
                self.assertEquals(field_value, self.employee_data[field_name])

        new_user_field_values = {k: v for k, v in new_user.__dict__.items() if k != '_state'}
        for field_name, field_value in new_user_field_values.items():
            if field_name in self.employee_data:
                self.assertEquals(field_value, self.employee_data[field_name])

        self.assertEquals(new_user.username, self.employee_data['email'])

    def test__register_employee_invalid_form__should_show_errors(self):
        invalid_data = {
            'email': 'invalid_email',
            'phone_number': '0894'
        }
        self.client.force_login(self.user)
        self.employee_data.update(invalid_data)
        response = self.client.post(self.url, data=self.employee_data)

        self.assertEquals(response.status_code, 200)

        form = response.context['form']
        self.assertEquals(len(form.errors), len(invalid_data))
        self.assertEquals(
            form.errors['email'],
            ['Enter a valid email address.']
        )
        self.assertEquals(
            form.errors['phone_number'],
            ['Enter a valid phone number (e.g. 02 123 456) or a number with an international call prefix.']
        )

