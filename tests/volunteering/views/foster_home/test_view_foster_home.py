from django.test import TestCase, Client
from django.urls import reverse

from PAWesome.volunteering.views import ViewFosterHomes
from tests.setup import _create_user_with_organization_profile, _create_foster_home


class TestViewFosterHome(TestCase):
    def setUp(self):
        self.user, self.organization, _ = _create_user_with_organization_profile()

        self.foster_home_1 = _create_foster_home()
        self.foster_home_2 = _create_foster_home(email='test_foster_home_2@gmail.com')

        self.url = reverse('foster-homes')
        self.client = Client()

    def test__view_foster_homes_not_authenticated__should_redirect_to_login(self):
        response = self.client.get(self.url)

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('login') + f'?next={self.url}')

    def test__view_foster_homes__should_show_all_objects(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, ViewFosterHomes.template_name)

        self.assertQuerysetEqual(
            response.context['object_list'],
            [self.foster_home_1, self.foster_home_2],
            ordered=False
        )
