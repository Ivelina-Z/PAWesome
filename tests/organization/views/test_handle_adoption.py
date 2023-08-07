from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase, Client
from django.urls import reverse

from PAWesome.adoption.models import AdoptionSurvey, SubmittedAdoptionSurvey
from PAWesome.animal.models import AdoptedAnimalsArchive, AdoptedAnimalPhotosArchive, AnimalPhotos
from tests.setup import _create_user_with_organization_profile, _create_animal, _instance_dict_no_state, \
    _create_main_photo


class TestHandleAdoption(TestCase):
    def setUp(self):
        self.user, self.organization, self.group = _create_user_with_organization_profile(
            ['add_adoptedanimalsarchive']
        )

        self.adoption_form = AdoptionSurvey.objects.create(
            questionnaire_text={
                "firstName": "", "lastName": "", "Question 1": ""
            },
            created_by=self.organization
        )

        valid_filled_form = {
            'email': 'adopter1@gmail.com',
            'phone_number': '0894112233',
            "firstName": "Test name",
            "lastName": "Test Last Name",
            "Question 1": "Test answer 1"
        }
        self.animal = _create_animal(self.organization)
        self.animal_photo = _create_main_photo(self.animal)

        submit_form_response = self.client.post(
            reverse('submit-adopt-form', kwargs={'pk': self.animal.pk}),
            data=valid_filled_form
        )

        self.submitted_form = SubmittedAdoptionSurvey.objects.get(animal=self.animal.pk)
        self.url = reverse(
            'organization-handle-adoption-forms',
            kwargs={'slug': self.organization.slug, 'pk': self.submitted_form.pk}
        )

        self.client = Client()

    def test__handle_adoption_form_post_get_no_authorization__should_redirect_to_login(self):
        response = self.client.get(self.url)

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('login') + f'?next={self.url}')

    def test__handle_adoption_form_post_post_no_authorization__should_redirect_to_login(self):
        response = self.client.post(self.url)

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('login') + f'?next={self.url}')

    def test__handle_adoption_form_post_no_permissions__should_return_403(self):
        self.user.groups.remove(self.group)
        self.client.force_login(self.user)
        response = self.client.post(self.url)

        self.assertEquals(response.status_code, 403)

    def test__handle_adoption_form_post_adopt_action__should_move_animal_and_photos_to_archive(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url, data={'action': 'adopt'})

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse('dashboard', kwargs={'slug': self.organization.slug})
        )

        with self.assertRaises(ObjectDoesNotExist) as e:
            SubmittedAdoptionSurvey.objects.get(pk=self.submitted_form.pk)
        self.assertIsNotNone(e)

        archived_animal = AdoptedAnimalsArchive.objects.get(name=self.animal.name)
        archived_animal_data = _instance_dict_no_state(
            archived_animal.__dict__,
            keys_to_del=['_state', 'id', 'date_of_adoption']
        )
        expected_animal_data = _instance_dict_no_state(self.animal.__dict__, keys_to_del=['_state', 'id'])
        clean_submitted_form_data = _instance_dict_no_state(
            self.submitted_form.__dict__,
            keys_to_del=['_state', 'id', 'animal_id', 'organization_id', 'status']
        )
        expected_animal_data.update(clean_submitted_form_data)
        self.assertEquals(archived_animal_data, expected_animal_data)

        with self.assertRaises(ObjectDoesNotExist) as e:
            AnimalPhotos.objects.get(animal=self.animal.pk)
        self.assertIsNotNone(e)

        archived_animal_photo = AdoptedAnimalPhotosArchive.objects.get(animal=self.animal.pk)
        self.assertEqual(
            self.animal_photo.photo.read(),
            archived_animal_photo.photo.read()
        )

        with self.assertRaises(ObjectDoesNotExist) as e:
            SubmittedAdoptionSurvey.objects.get(pk=self.submitted_form.pk)
        self.assertIsNotNone(e)

    def test__handle_adoption_form_post_reject_action__should_delete_survey_and_sent_mail(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url, data={'action': 'reject'})

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse('dashboard', kwargs={'slug': self.organization.slug})
        )

        with self.assertRaises(ObjectDoesNotExist) as e:
            SubmittedAdoptionSurvey.objects.get(pk=self.submitted_form.pk)
        self.assertIsNotNone(e)
