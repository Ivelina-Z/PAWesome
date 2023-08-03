from django.test import TestCase, Client
from django.urls import reverse

from PAWesome.volunteering.forms import FosterHomeForm
from PAWesome.volunteering.models import FosterHome
from PAWesome.volunteering.views import EditFosterHome
from tests.setup import _create_foster_home


class TestEditFosterHome(TestCase):
    def setUp(self):
        self.foster_home = _create_foster_home()

        self.url = reverse('foster-home-edit', kwargs={'token': self.foster_home.token})
        self.client = Client()

    def test__valid_token_for_edit__should_render_the_page(self):
        response = self.client.get(self.url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, EditFosterHome.template_name)

    def test__invalid_token_for_edit__should_return_404(self):
        response = self.client.get(reverse(
            'foster-home-edit',
            kwargs={'token': 'invalid1test2token3'}
        ))

        self.assertEquals(response.status_code, 404)

    def test__edit_valid_form_data__should_update_the_object(self):
        valid_update_data = {
            'phone_number': self.foster_home.phone_number,
            'email': self.foster_home.email,
            'cat_available_spots': 1,
            'dog_available_spots': 1,
            'bunny_available_spots': self.foster_home.bunny_available_spots,
            'additional_info': self.foster_home.additional_info,
            'location': 'POINT(42.0 27.0)',
            'token': self.foster_home.token
        }

        response = self.client.post(self.url, data=valid_update_data)

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, EditFosterHome.success_url)

        updated_foster_home = FosterHome.objects.get(pk=self.foster_home.pk)
        self.assertEquals(updated_foster_home.pk, self.foster_home.pk)
        self.assertEquals(updated_foster_home.token, self.foster_home.token)
        self.assertEquals(updated_foster_home.cat_available_spots, valid_update_data['cat_available_spots'])
        self.assertEquals(updated_foster_home.dog_available_spots, valid_update_data['dog_available_spots'])

    def test__edit_invalid_form_data__should_render_the_form_with_errors(self):
        valid_update_data = {
            'phone_number': '0894',
            'email': self.foster_home.email,
            'cat_available_spots': 2,
            'dog_available_spots': self.foster_home.dog_available_spots,
            'bunny_available_spots': self.foster_home.bunny_available_spots,
            'additional_info': self.foster_home.additional_info,
            'location': 'POINT(42.0 27.0)',
            'token': self.foster_home.token
        }

        response = self.client.post(self.url, data=valid_update_data)
        self.assertEquals(response.status_code, 200)
        form = response.context['form']
        self.assertEquals(len(form.errors), 1)
        self.assertEquals(
            form.errors['phone_number'],
            ['Enter a valid phone number (e.g. 02 123 456) or a number with an international call prefix.']
        )

    def test__edit_no_available_spots_fields__should_render_the_form_with_errors(self):
        valid_update_data = {
            'phone_number': self.foster_home.phone_number,
            'email': self.foster_home.email,
            'cat_available_spots': 0,
            'dog_available_spots': self.foster_home.dog_available_spots,
            'bunny_available_spots': self.foster_home.bunny_available_spots,
            'additional_info': self.foster_home.additional_info,
            'location': 'POINT(42.0 27.0)',
            'token': self.foster_home.token
        }

        response = self.client.post(self.url, data=valid_update_data)
        self.assertEquals(response.status_code, 200)
        form = response.context['form']
        self.assertEquals(form.errors['__all__'][0], FosterHomeForm.ERROR_MESSAGE)
