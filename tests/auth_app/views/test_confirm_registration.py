from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase, Client
from django.urls import reverse

from tests.setup import _create_user_with_organization_profile


class TestConfirmRegistration(TestCase):
    def setUp(self):
        self.user, self.organization, _ = _create_user_with_organization_profile(['add_employee', 'add_customuser'])

        self.employee_group = Group.objects.create(name='Employees')
        self.employee_data = {
            'first_name': 'Test First Name',
            'last_name': 'Test Last Name',
            'email': 'test@mail.com',
            'phone_number': '0894001122',
            'password1': 'testpass',
            'password2': 'testpass'
        }

        self.user_model = get_user_model()
        self.client = Client()

    def test__valid_token__should_activate_the_user_and_delete_token(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('organization-register-employee'), data=self.employee_data)

        new_user = self.user_model.objects.get(email=self.employee_data['email'])
        self.assertTrue(new_user.confirmation_token)
        self.assertFalse(new_user.is_active)

        response_confirmation_post = self.client.get(
            reverse('register-confirmation', kwargs={'token': new_user.confirmation_token})
        )
        self.assertEquals(response_confirmation_post.status_code, 302)
        self.assertRedirects(response_confirmation_post, reverse('login'))
        new_user.refresh_from_db()
        self.assertFalse(new_user.confirmation_token)
        self.assertTrue(new_user.is_active)

    def test__invalid_token__should_raise_404(self):
        self.client.force_login(self.user)
        invalid_token = 'test-token-123'

        response = self.client.post(reverse('organization-register-employee'), data=self.employee_data)

        new_user = self.user_model.objects.get(email=self.employee_data['email'])
        self.assertTrue(new_user.confirmation_token)
        self.assertFalse(new_user.is_active)
        response_confirmation_post = self.client.get(
            reverse('register-confirmation', kwargs={'token': invalid_token})
        )
        self.assertEquals(response_confirmation_post.status_code, 404)
