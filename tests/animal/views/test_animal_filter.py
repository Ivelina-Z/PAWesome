from django.urls import reverse

from django.contrib.gis.geos import Point
from django.test import TestCase, Client

from PAWesome.animal.models import Animal
from tests.setup import _create_user_with_organization_profile, _create_animal


class TestAnimalFilter(TestCase):
    def setUp(self) -> None:
        _, self.organization, _ = _create_user_with_organization_profile()

        animal_cat_female_sprayed_unknown_vaccinated = _create_animal(
            self.organization,
            name='Test Animal 1',
            animal_type='cat',
            gender='female',
            sprayed=None
        )

        animal_dog_male_sprayed_vaccinated_unknown = _create_animal(
            self.organization,
            name='Test Animal 2',
            animal_type='dog',
            gender='male',
            vaccinated=None
        )

        animal_bunny_female_sprayed_vaccinated = _create_animal(
            self.organization,
            name='Test Animal 3',
            animal_type='bunny',
            gender='female'
        )

        self.all_animals = [
            animal_cat_female_sprayed_unknown_vaccinated,
            animal_dog_male_sprayed_vaccinated_unknown,
            animal_bunny_female_sprayed_vaccinated
        ]
        self.query_string = {'animal_type': 'all', 'gender': 'all', 'sprayed': 'all', 'vaccinated': 'all'}

        self.client = Client()

    def test__filter_by_gender_male__should_render_only_male(self):
        filtered_male_animals = list(filter(lambda animal: animal.gender == 'male', self.all_animals))
        self.query_string.update({'gender': 'male'})
        response = self.client.get(reverse('animals-all'), self.query_string)
        self.assertQuerysetEqual(response.context['object_list'], filtered_male_animals)

    def test__filter_by_animal_type_bunny__should_render_only_bunny(self):
        filtered_bunnies = list(filter(lambda animal: animal.animal_type == 'bunny', self.all_animals))
        self.query_string.update({'animal_type': 'bunny'})
        response = self.client.get(reverse('animals-all'), self.query_string)
        self.assertQuerysetEqual(response.context['object_list'], filtered_bunnies)

    def test__filter_by_sprayed_true__should_render_only_sprayed(self):
        filtered_sprayed_true = list(filter(lambda animal: animal.sprayed is True, self.all_animals))
        self.query_string.update({'sprayed': 'True'})
        response = self.client.get(reverse('animals-all'), self.query_string)
        self.assertQuerysetEqual(response.context['object_list'], filtered_sprayed_true)

    def test__filter_by_sprayed_none__should_render_only_sprayed_unknown(self):
        filtered_sprayed_unknown = list(filter(lambda animal: animal.sprayed is None, self.all_animals))
        self.query_string.update({'sprayed': ''})
        response = self.client.get(reverse('animals-all'), self.query_string)
        self.assertQuerysetEqual(response.context['object_list'], filtered_sprayed_unknown)

    def test__filter_by_vaccinated_none__should_render_only_vaccinated_unknown(self):
        filtered_vaccinated_unknown = list(filter(lambda animal: animal.vaccinated is None, self.all_animals))
        self.query_string.update({'vaccinated': ''})
        response = self.client.get(reverse('animals-all'), self.query_string)
        self.assertQuerysetEqual(response.context['object_list'], filtered_vaccinated_unknown)

    def test__filter_by_vaccinated_true__should_render_only_vaccinated(self):
        filtered_vaccinated = list(filter(lambda animal: animal.vaccinated is True, self.all_animals))
        self.query_string.update({'vaccinated': True})
        response = self.client.get(reverse('animals-all'), self.query_string)
        self.assertQuerysetEqual(response.context['object_list'], filtered_vaccinated)

    def test__filter_by_bunny_sprayed_true_vaccinated_true_female__should_render_bunny_sprayed_vaccinated_female(self):
        filtered_by_all_fields = list(filter(lambda animal: (
            animal.animal_type == 'bunny' and
            animal.sprayed is True and
            animal.vaccinated is True and
            animal.gender == 'female'
        ), self.all_animals))
        self.query_string.update({'animal_type': 'bunny', 'sprayed': True, 'vaccinated': True, 'gender': 'female'})
        response = self.client.get(reverse('animals-all'), self.query_string)
        self.assertQuerysetEqual(response.context['object_list'], filtered_by_all_fields)
