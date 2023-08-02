from django.test import TestCase, Client
from django.urls import reverse

from PAWesome.adoption.models import AdoptionSurvey, SubmittedAdoptionSurvey
from tests.setup import _create_user_with_organization_profile, _create_animal


class TestAnimalDetails(TestCase):
    def setUp(self):
        self.user, self.organization, _ = _create_user_with_organization_profile()
        _, self.other_organization, _ = _create_user_with_organization_profile(email='testuserother@test.com')

        self.adoption_form = AdoptionSurvey.objects.create(
            questionnaire_text={
                "firstName": "", "lastName": "", "Question 1": ""
            },
            created_by=self.organization
        )
        self.adoption_form_other_organization = AdoptionSurvey.objects.create(
            questionnaire_text={
                "firstName": "", "lastName": "", "Question other": ""
            },
            created_by=self.other_organization
        )

        self.animal_1 = _create_animal(self.organization)
        self.animal_other_organization = _create_animal(self.other_organization)

        valid_filled_form = {
            'email': 'adopter1@gmail.com',
            'phone_number': '0894112233',
            "firstName": "Test name",
            "lastName": "Test Last Name",
            "Question 1": "Test answer 1"
        }
        self.client.post(
            reverse('submit-adopt-form', kwargs={'pk': self.animal_1.pk}),
            data=valid_filled_form
        )

        valid_filled_form_other = {
            'email': 'adopter1@gmail.com',
            'phone_number': '0894112233',
            "firstName": "Test name",
            "lastName": "Test Last Name",
            "Question Other": "Test answer other"
        }
        self.client.post(
            reverse('submit-adopt-form', kwargs={'pk': self.animal_other_organization.pk}),
            data=valid_filled_form_other
        )

        self.url = reverse(
            'organization-pending-adoption-forms',
            kwargs={'slug': self.organization.slug}
        )

        self.client = Client()

    def test__pending_adopt_forms_not_authenticated__should_redirect_to_login(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('login') + f'?next={self.url}')

    def test__pending_adopt_forms__should_return_only_the_organization_forms(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)

        self.assertEquals(response.status_code, 200)

        self.expected_query_set = SubmittedAdoptionSurvey.objects.filter(organization=self.organization)
        self.assertQuerysetEqual(
            response.context['object_list'],
            self.expected_query_set
        )
