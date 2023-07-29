from django.contrib.gis.geos import Point
from django.test import TestCase, Client
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

from PAWesome.adoption.views import SubmitAdoptForm
from PAWesome.adoption.models import AdoptionSurvey, SubmittedAdoptionSurvey
from PAWesome.animal.models import Animal
from tests.adoption.setup import _create_user_with_organization_profile


class TestSubmitAdoptForm(TestCase):
    def setUp(self) -> None:
        _, self.organization, _ = _create_user_with_organization_profile()
        self.QUESTIONS = ['Question 1', 'Question 2', 'Question 3']
        self.INITIAL_QUESTIONS = {q: '' for q in self.QUESTIONS}

        self.adoption_survey = AdoptionSurvey.objects.create(
            questionnaire_text=self.INITIAL_QUESTIONS,
            created_by=self.organization
        )

        self.animal = Animal.objects.create(
            name='Test Animal',
            animal_type='cat',
            gender='male',
            sprayed=True,
            vaccinated=True,
            current_residence='street',
            location=Point(42.0, 27.0),
            organization=self.organization
        )
        self.client = Client()

    def test_render_correct_fields__should_create_fields_from_questionnaire_text(self):
        response = self.client.get(
            reverse('submit-adopt-form', kwargs={'pk': self.animal.pk})
        )

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, SubmitAdoptForm.template_name)

        form = response.context['form']
        for idx, field in enumerate(form):
            if idx == 0:
                self.assertEquals(field.name, 'email')
            elif idx == 1:
                self.assertEquals(field.name, 'phone_number')
            else:
                self.assertEquals(field.name, self.QUESTIONS[idx - 2])

    def test__submit_valid_form__should_redirect_to_homepage(self):
        valid_filled_form = {
            'email': 'testmail@mail.com',
            'phone_number': '0894001122',
            'Question 1': 'Answer 1',
            'Question 2': 'Answer 2',
            'Question 3': 'Answer 3'
        }

        response = self.client.post(
            reverse('submit-adopt-form', kwargs={'pk': self.animal.pk}),
            data=valid_filled_form
        )

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('homepage'))

        all_submitted_adoption_forms = SubmittedAdoptionSurvey.objects.all()
        self.assertEquals(len(all_submitted_adoption_forms), 1)

        submitted_adoption_form = all_submitted_adoption_forms.first()
        self.assertEquals(submitted_adoption_form.email, valid_filled_form['email'])
        self.assertEquals(submitted_adoption_form.phone_number, valid_filled_form['phone_number'])
        for question, answer in submitted_adoption_form.questionnaire_text.items():
            self.assertEquals(answer, valid_filled_form[question])

    def test__submit_invalid_form__should_show_errors_in_form_page(self):
        client_path = reverse('submit-adopt-form', kwargs={'pk': self.animal.pk})
        invalid_filled_form = {
            'email': '',
            'phone_number': '0894001122',
            'Question 1': 'Answer 1',
            'Question 2': 'Answer 2',
            'Question 3': 'Answer 3'
        }

        response = self.client.post(client_path, data=invalid_filled_form)
        form = response.context['form']
        self.assertTrue(form.errors['email'])
        self.assertFalse(form.is_valid())

        with self.assertRaises(ObjectDoesNotExist) as e:
            SubmittedAdoptionSurvey.objects.get(pk=self.adoption_survey.pk)

        self.assertIsNotNone(e.exception)

