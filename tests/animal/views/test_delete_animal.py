from django.core.exceptions import ObjectDoesNotExist
from django.db import connection
from django.urls import reverse

from django.test import TestCase, Client

from PAWesome.animal.models import Animal
from tests.setup import _create_animal, _create_user_with_organization_profile


class TestAnimalDelete(TestCase):
    def setUp(self):
        self.user, self.organization, self.group = _create_user_with_organization_profile(
            ['delete_animal', 'delete_animalphotos']
        )
        self.animal = _create_animal(self.organization)
        self.url = reverse('animal-delete', kwargs={'pk': self.animal.pk})

        self.client = Client()

    def test__animal_delete_unauthorized__should_redirect_to_login(self):
        response = self.client.post(self.url)

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse('login') + f'?next={self.url}'
        )

    def test__animal_delete_no_permissions__should_return_404(self):
        self.user.groups.remove(self.group)
        self.client.force_login(self.user)
        response = self.client.post(self.url)

        self.assertEquals(response.status_code, 404)

    def test__animal_delete__should_delete_animal(self):
        self.client.force_login(self.user)

        initial_queries_count = len(connection.queries)
        response = self.client.post(self.url)
        final_num_queries = len(connection.queries)

        self.assertEquals(initial_queries_count, final_num_queries)
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse('organization-animals', kwargs={'slug': self.organization.slug})
        )

        with self.assertRaises(ObjectDoesNotExist) as e:
            Animal.objects.get(pk=self.animal.pk)
        self.assertIsNotNone(e)

