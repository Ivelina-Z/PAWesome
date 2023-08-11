from django.test import TestCase, Client
from django.urls import reverse

from PAWesome.organization.models import Employee
from tests.setup import _create_user_with_organization_profile, _create_animal


class TestListAnimals(TestCase):
    def setUp(self):
        self.user, self.organization, _ = _create_user_with_organization_profile()
        _, self.other_organization, _ = _create_user_with_organization_profile(email='testuserother@test.com')

        self.animal_1 = _create_animal(self.organization)
        self.animal_2 = _create_animal(self.organization)
        self.animal_other_organization = _create_animal(self.other_organization)

        self.url = reverse(
            'organization-animals',
            kwargs={'slug': self.organization.slug}
        )
        self.client = Client()

    def test__all_animals_not_authenticated__should_redirect_to_login(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('login') + f'?next={self.url}')

    def test__get_all_animals__should_return_only_the_organization_animals(self):
        self.client.force_login(self.user)
        query_params = {
            'gender': 'all',
            'sprayed': 'all',
            'vaccinated': 'all',
        }
        response = self.client.get(self.url, data=query_params)

        self.assertEquals(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['object_list'],
            [self.animal_1, self.animal_2]
        )
