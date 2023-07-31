# from django.contrib.gis.geos import Point
# from django.core.exceptions import ObjectDoesNotExist
# from django.core.files.uploadedfile import SimpleUploadedFile
# from django.urls import reverse
#
# from django.test import TestCase, Client
#
# from PAWesome.animal.forms import AnimalForm, AnimalPhotoForm
# from PAWesome.animal.models import AnimalPhotos, Animal
# from PAWesome.animal.views import AddAnimalView
# from tests.setup import _create_user_with_organization_profile, _create_animal, _create_main_photo
#
#
# class TestAnimalDetails(TestCase):
#     def setUp(self):
#         self.user, self.organization, _ = _create_user_with_organization_profile()
#         self.image = SimpleUploadedFile(
#                 'test_photo.jpg',
#                 b'This is a test photo.',
#                 content_type='image/jpeg')
#         self.animal_data = {
#             'organization': self.organization,
#             'name': 'Test Animal 1',
#             'animal_type': 'cat',
#             'gender': 'male',
#             'sprayed': True,
#             'vaccinated': True,
#             'medical_issues': '',
#             'current_residence': 'street',
#             'location': 'POINT (42.0 27.0)'
#         }
#         self.animal_photo_data = {
#             'animalphotos_set-TOTAL_FORMS': '1',
#             'animalphotos_set-INITIAL_FORMS': '0',
#             'animalphotos_set-MIN_NUM_FORMS': '0',
#             'animalphotos_set-MAX_NUM_FORMS': '1000',
#             'animalphotos_set-0-photo': 'media/images/_36e365ca-55dd-44f8-8ad8-d994390780f3.jpeg'
#         }
#         self.url = reverse('animal-add')
#         self.client = Client()
#
#     def test__animal_add_unauthorized_user__should_redirect_to_login(self):
#         response = self.client.get(self.url)
#         self.assertEquals(response.status_code, 302)
#         self.assertRedirects(response, reverse('login') + f'?next={self.url}')
#
#     def test__formset_get__should_render_empty_formset(self):
#         self.client.force_login(self.user)
#         response = self.client.get(self.url)
#         form = response.context['form']
#         formset = form.formset
#
#         self.assertEquals(response.status_code, 200)
#
#         self.assertIsInstance(form, AnimalForm)
#         self.assertIsInstance(formset, AddAnimalView.AnimalPhotoFormSet)
#         self.assertIsInstance(formset.forms[0], AnimalPhotoForm)
#
#         self.assertEquals(len(formset.forms), AddAnimalView.AnimalPhotoFormSet.extra)
#
#     def get_form_data(self):
#         # Create instances of Animal and AnimalPhotos forms
#         animal_form = AnimalForm(data=self.animal_data)
#         formset = AddAnimalView.AnimalPhotoFormSet(data=self.animal_photo_data, instance=animal_form.instance)
#
#         # Retrieve the formset data as a dictionary
#         formset_data = formset.management_form.cleaned_data
#         for i, form in enumerate(formset):
#             for field_name, field_value in form.data.items():
#                 formset_data[f'form-{i}-{field_name}'] = field_value
#
#         return formset_data
#
#     def test__valid_formset_post__should_create_animal(self):
#         self.client.force_login(self.user)
#
#         form = AnimalForm(data=self.animal_data)
#         form.formset = AddAnimalView.AnimalPhotoFormSet(data=[self.animal_photo_data])
#
#         # Combine form and formset data into a single dictionary
#         # form_data = {**form.data, **form.formset[0].data}
#         response = self.client.post(self.url, data=self.get_form_data())
#
#         # self.assertEquals(response.status_code, 302)
#         # self.assertRedirects(
#         #     response,
#         #     reverse('dashboard', kwargs={'slug': self.organization.slug})
#         # )
#
#         print(Animal.objects.all())
#         created_animal = Animal.objects.get(name=self.animal_data['name'])
#         print(AnimalPhotos.objects.all())
#         created_photo = AnimalPhotos.objects.get(animal=created_animal.pk)
#
#         # created_animal_dict = {k: v for k, v in created_animal.__dict__.items() if k != '_state'}
#         # self.assertEquals(self.animal_data, created_animal_dict)
#         #
#         # created_photo_dict = {k: v for k, v in created_photo.__dict__.items() if k != '_state'}
#         # self.assertEquals(self.animal_photo_data, created_photo_dict)
#
#     # def test__invalid_animal_form_no_animal_type__should_render_formset_invalid(self):
#     #     self.client.force_login(self.user)
#     #     invalid_animal_form = {
#     #         'organization': self.organization,
#     #         'name': 'Test Animal 1',
#     #         'animal_type': '',
#     #         'gender': 'male',
#     #         'sprayed': True,
#     #         'vaccinated': True,
#     #         'medical_issues': '',
#     #         'current_residence': 'street',
#     #         'location': Point(42.0, 27.0),
#     #     }
#     #
#     #     self.formset_data['form-0-animal'] = invalid_animal_form
#     #
#     #     response = self.client.post(self.url, data=self.formset_data)
#     #     self.assertEquals(response.status_code, 200)
#     #
#     #     form = response.context['form']
#     #     self.assertTrue(form.errors['photo'])
#     #     self.assertFalse(form.is_valid())
#     #
#     #     with self.assertRaises(ObjectDoesNotExist) as e:
#     #         Animal.objects.get(name=invalid_animal_form['name'])
#     #     self.assertIsNotNone(e.exception)
#
#     # def test__invalid_photo_form_no_photo__should_render_formset_invalid(self):
#     #     self.client.force_login(self.user)
#     #     invalid_animal_photo_form = {
#     #         'animal': self.animal.pk,
#     #         'photo': SimpleUploadedFile("empty.jpg", b""),
#     #         'is_main_image': True
#     #     }
#     #
#     #     self.formset_data['form-0-animal_photo'] = invalid_animal_photo_form
#     #
#     #     response = self.client.post(self.url, data=self.formset_data)
#     #     self.assertEquals(response.status_code, 200)
#     #
#     #     form = response.context['form']
#     #     errors = form.errors
#     #     print(errors)
#     #     # self.assertTrue('__all__' in form.errors)
#     #     self.assertFalse(form.is_valid())
#     #
#     #     with self.assertRaises(ObjectDoesNotExist) as e:
#     #         AnimalPhotos.objects.get(animal=self.animal.pk)
#     #     self.assertIsNotNone(e.exception)
