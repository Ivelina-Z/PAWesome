from django.test import TestCase, Client
from django.urls import reverse

from PAWesome.adoption.models import AdoptionSurvey
from PAWesome.adoption.views import INITIAL_FORMS
from tests.setup import _create_user_with_organization_profile


class AddAdoptionFormViewTest(TestCase):
    FORMSET_DATA = {
        'form-TOTAL_FORMS': 2,
        'form-INITIAL_FORMS': 0,
        'form-MIN_NUM_FORMS': 0,
        'form-MAX_NUM_FORMS': 1000,
        'form-0-question': 'Question 1',
        'form-1-question': 'Question 2'
    }

    def setUp(self):
        self.user, self.organization, self.group = _create_user_with_organization_profile(['add_adoptionsurvey'])
        self.client = Client()

    def test__add_adoption_form_view__should_render_template(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('adopt-form-add'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'adopt-form-add.html')

    def test__add_adoption_form_view_no_permission__should_return_forbidden(self):
        self.user.groups.remove(self.group)
        self.client.force_login(self.user)
        response = self.client.get(reverse('adopt-form-add'))
        self.assertEquals(response.status_code, 403)
        self.assertTemplateNotUsed(response, 'adopt-form-add.html')

    def test__add_adoption_form_view_not_authenticated__should_redirect(self):
        next_url = reverse('adopt-form-add')
        response = self.client.get(reverse('adopt-form-add'))
        self.assertRedirects(response, reverse('login') + f'?next={next_url}')

    def test__formset_is_in_get_context__should_render_template(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('adopt-form-add'))
        self.variable_in_context = {'formset': self.FORMSET_DATA}
        formset = response.context['formset']
        self.assertIsNotNone(formset)

    def test__formset_valid_data_total_forms_initial__should_save(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('adopt-form-add'), data=self.FORMSET_DATA)

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard', kwargs={'slug': self.organization.slug}))

        self.assertEquals(len(AdoptionSurvey.objects.all()), 1)
        adoption_survey = AdoptionSurvey.objects.first()
        questionnaire_text_expected = {
             'Question 1': '',
             'Question 2': ''
        }

        self.assertEquals(adoption_survey.questionnaire_text, questionnaire_text_expected)
        self.assertEquals(adoption_survey.created_by, self.organization)

    def test__formset_valid_data_total_forms_plus_one__should_save(self):
        self.client.force_login(self.user)
        formset_plus_one_form = self.FORMSET_DATA.copy()
        formset_plus_one_form.update({'form-2-question': 'Question 3'})
        formset_plus_one_form['form-TOTAL_FORMS'] += 1

        response = self.client.post(reverse('adopt-form-add'), data=formset_plus_one_form)

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard', kwargs={'slug': self.organization.slug}))

        self.assertEquals(len(AdoptionSurvey.objects.all()), 1)
        adoption_survey = AdoptionSurvey.objects.first()
        questionnaire_text_expected = {
            'Question 1': '',
            'Question 2': '',
            'Question 3': ''
        }

        self.assertEquals(adoption_survey.questionnaire_text, questionnaire_text_expected)
        self.assertEquals(adoption_survey.created_by, self.organization)

    # def test__formset_invalid_data__should_redirect(self):
    #     self.client.force_login(self.user)
    #     formset_invalid = self.FORMSET_DATA.copy()
    #     formset_invalid.update({'form-3-question': 'Question 4'})
    #     response = self.client.post(reverse('adopt-form-add'), data=formset_invalid)
    #
    #     self.assertEquals(response.status_code, 302)
    #     self.assertRedirects(response, reverse('adopt-form-add'))
    #
    #     self.assertEquals(len(AdoptionSurvey.objects.all()), 0)
