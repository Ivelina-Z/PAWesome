from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase, Client
from django.urls import reverse

from PAWesome.volunteering.forms import FosterHomeForm
from PAWesome.volunteering.models import FosterHome


class TestAddFosterHome(TestCase):
    def setUp(self):
        self.url = reverse('foster-home-add')
        self.client = Client()

    def test__add_foster_home_valid_form__should_add_foster_home(self):
        valid_form_data = {
            'phone_number': '0894112233',
            'email': 'test_foster_home@gmail.com',
            'cat_available_spots': 2,
            'location': 'POINT(42.0 27.0)',
        }
        response = self.client.post(self.url, data=valid_form_data)

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('homepage'))

        self.assertTrue(FosterHome.objects.filter(email=valid_form_data['email']).exists())
        new_foster_home = FosterHome.objects.get(email=valid_form_data['email'])
        self.assertIsNotNone(new_foster_home.token)

    def test__add_foster_home_invalid_form__should_render_form_with_errors(self):
        invalid_form_data = {
            'phone_number': '0894',
            'email': 'test_foster_home@gmail.com',
            'cat_available_spots': 2,
            'location': 'POINT(42.0 27.0)',
        }
        response = self.client.post(self.url, data=invalid_form_data)

        self.assertEquals(response.status_code, 200)
        form = response.context['form']
        self.assertEquals(
            form.errors['phone_number'],
            ['Enter a valid phone number (e.g. 02 123 456) or a number with an international call prefix.']
        )

        with self.assertRaises(ObjectDoesNotExist) as e:
            FosterHome.objects.get(email=invalid_form_data['email'])

    def test__add_foster_home_no_available_spot_field__should_render_form_with_errors(self):
        invalid_form_data = {
            'phone_number': '0894788733',
            'email': 'test_foster_home@gmail.com',
            'location': 'POINT(42.0 27.0)',
        }
        response = self.client.post(self.url, data=invalid_form_data)

        self.assertEquals(response.status_code, 200)
        form = response.context['form']
        self.assertIsNotNone(form.errors)
        self.assertEquals(form.errors['__all__'][0], FosterHomeForm.ERROR_MESSAGE)
