from django.urls import reverse

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client

from PAWesome.animal.models import AnimalPhotos
from tests.setup import _create_animal, _create_user_with_organization_profile


class TestAnimalDetails(TestCase):
    def setUp(self):
        _, self.organization, _ = _create_user_with_organization_profile()
        self.animal = _create_animal(self.organization)
        self.animal_photo_1 = AnimalPhotos.objects.create(
            animal=self.animal,
            photo=SimpleUploadedFile(
                'test_photo.jpg',
                b'This is a test photo.',
                content_type='image/jpeg'
            ),
            is_main_image=True
        )

        self.animal_photo_2 = AnimalPhotos.objects.create(
            animal=self.animal,
            photo=SimpleUploadedFile(
                'test_photo_2.jpg',
                b'This is second test photo.',
                content_type='image/jpeg'
            ),
            is_main_image=False
        )

        self.client = Client()

    def test__photos_are_prefetched__should_have_photo_in_context(self):
        response = self.client.get(reverse('animal-details', kwargs={'pk': self.animal.pk}))

        self.assertEquals(response.status_code, 200)

        animal = response.context['object']
        photos = animal.animalphotos_set.all().order_by('pk')
        self.assertEquals(len(photos), 2)
        self.assertQuerysetEqual(photos, AnimalPhotos.objects.filter(animal=self.animal.pk))
