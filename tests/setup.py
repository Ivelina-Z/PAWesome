from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission, Group
from django.contrib.gis.geos import Point
from django.core.files.uploadedfile import SimpleUploadedFile

from PAWesome.animal.models import Animal, AnimalPhotos
from PAWesome.organization.models import Organization


def _create_user_with_organization_profile(permission_codename=None):
    group = Group.objects.create(name='Organizations')
    if permission_codename:
        permission = Permission.objects.filter(codename__in=permission_codename).values_list('pk', flat=True)
        group.permissions.set(permission)

    UserModel = get_user_model()
    user = UserModel.objects.create(username='testuser@test.com', password='testpass')
    organization = Organization.objects.create(
        name='Test Organization',
        phone_number='+0894010101',
        email='testuser@test.com',
        slug='test-organization',
        user=user
    )
    user.groups.add(group)
    return user, organization, group

def _create_animal(
        organization,
        name='Test Animal',
        animal_type='cat',
        gender='male',
        sprayed=True,
        vaccinated=True,
        medical_issues='',
        current_residence='street',
        location=Point(42.0, 27.0),
):
    arguments = locals().copy()
    animal = Animal.objects.create(**arguments)
    return animal


def _create_main_photo(animal):
    photo = AnimalPhotos.objects.create(
        animal=animal,
        photo=SimpleUploadedFile(
            'test_photo.jpg',
            b'This is a test photo.',
            content_type='image/jpeg'
        ),
        is_main_image=True
    )
    return photo
