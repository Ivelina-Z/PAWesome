from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase, Client
from django.urls import reverse

from PAWesome.volunteering.models import FosterHome
from PAWesome.volunteering.views import DeleteFosterHome
from tests.setup import _create_foster_home


class TestDeleteFosterHome(TestCase):
    def setUp(self):
        self.foster_home = _create_foster_home()

        self.url = reverse('foster-home-delete', kwargs={'token': self.foster_home.token})
        self.client = Client()

    def test__delete_valid_token__should_delete(self):
        response = self.client.post(self.url)

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, DeleteFosterHome.success_url)

        with self.assertRaises(ObjectDoesNotExist) as e:
            FosterHome.objects.get(pk=self.foster_home.pk)
        self.assertIsNotNone(e)

    def test__invalid_token_for_edit__should_return_404(self):
        response = self.client.get(reverse(
            'foster-home-delete',
            kwargs={'token': 'invalid1test2token3'}
        ))

        self.assertEquals(response.status_code, 404)
