from django.test import TestCase, Client
from django.urls import reverse

from PAWesome.adoption.forms import AdoptionSurveyForm
from PAWesome.adoption.models import AdoptionSurvey
from PAWesome.adoption.views import AdoptionSurveyFormSet, INITIAL_FORMS
from tests.setup import _create_user_with_organization_profile


class EditAdoptionFormViewTest(TestCase):

    def setUp(self):
        self.user, self.organization, self.group = _create_user_with_organization_profile(['change_adoptionsurvey'])

        self.QUESTIONS = ['Question 1', 'Question 2']
        self.INITIAL_QUESTIONS = {q: '' for q in self.QUESTIONS}

        self.adoption_survey = AdoptionSurvey.objects.create(
            questionnaire_text=self.INITIAL_QUESTIONS,
            created_by=self.organization
        )

        self.INITIAL_FORMS_DATA = [{'question': q} for q in self.QUESTIONS]
        self.formset = AdoptionSurveyFormSet(initial=self.INITIAL_FORMS_DATA)
        self.client = Client()

    def test__edit_adoption_form_view_no_permission__should_return_forbidden(self):
        self.user.groups.remove(self.group)
        self.client.force_login(self.user)
        response = self.client.get(
            reverse('adopt-form-edit'),
            kwargs={'pk': self.adoption_survey.pk}
        )

        self.assertEquals(response.status_code, 403)
        self.assertTemplateNotUsed(response, 'adopt-form-edit.html')

    def test__edit_adoption_form_view_not_authenticated__should_redirect(self):
        response = self.client.get(
            reverse('adopt-form-edit'),
            kwargs={'pk': self.adoption_survey.pk}
        )

        self.assertEquals(response.status_code, 302)
        next_url = reverse('adopt-form-edit')
        self.assertRedirects(response, reverse('login') + f'?next={next_url}')

    def test__edit_adoption_form_view__should_render_template(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse('adopt-form-edit'),
            kwargs={'pk': self.adoption_survey.pk}
        )
        self.variable_in_context = self.formset

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'adopt-form-edit.html')

        self.assertIn('formset', response.context)
        response_formset = response.context['formset']
        self.assertEqual(len(response_formset.forms), len(self.QUESTIONS))

        for idx, form in enumerate(response_formset):
            self.assertIsInstance(form, AdoptionSurveyForm)
            self.assertEqual(form.initial['question'], self.INITIAL_FORMS_DATA[idx]['question'])

    def test__edit_adoption_form_with_valid_change__should_change_instance(self):
        self.client.force_login(self.user)
        updated_formset_data = {
            'form-TOTAL_FORMS': 2,
            'form-INITIAL_FORMS': 0,
            'form-MIN_NUM_FORMS': 0,
            'form-MAX_NUM_FORMS': 1000,
            'form-0-question': 'Updated Question 1',
            'form-1-question': 'Question 2'
        }

        response = self.client.post(
            reverse('adopt-form-edit'),
            kwargs={'pk': self.adoption_survey.pk},
            data=updated_formset_data
        )

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard', kwargs={'slug': self.organization.slug}))

        updated_adoption_survey = AdoptionSurvey.objects.get(pk=self.adoption_survey.pk)
        self.assertEquals(
            updated_adoption_survey.questionnaire_text,
            {'Updated Question 1': '', 'Question 2': ''}
        )

    # def test__edit_adoption_form_with_invalid_change__should_render_the_formset(self):
    #     self.client.force_login(self.user)
    #     invalid_formset_data = {
    #         'form-TOTAL_FORMS': 3,
    #         'form-INITIAL_FORMS': 0,
    #         'form-MIN_NUM_FORMS': 0,
    #         'form-MAX_NUM_FORMS': 1000,
    #         'form-0-question': 'Question 1',
    #         'form-1-question': 'Question 2',
    #         'form-2-question': 'Question 3',
    #         'form-3-question': ''
    #     }
    #
    #     response = self.client.post(
    #         reverse('adopt-form-edit'),
    #         kwargs={'pk': self.adoption_survey.pk},
    #         data=invalid_formset_data
    #     )
    #
    #     self.assertEquals(response.status_code, 302)
    #     self.assertRedirects(response, reverse('adopt-form-edit'))

