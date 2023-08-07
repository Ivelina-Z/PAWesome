from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission, Group
from django.contrib.gis.geos import Point
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.text import slugify

from PAWesome.animal.models import Animal, AnimalPhotos
from PAWesome.organization.models import Organization
from PAWesome.volunteering.models import FosterHome, DonationTickets, DonationsDeliveryInfo


def _create_user_with_organization_profile(permission_codename=None, email='testuser@test.com'):
    try:
        group = Group.objects.get(name='Organizations')
    except Group.DoesNotExist:
        group = Group.objects.create(name='Organizations')

    if permission_codename:
        permission = Permission.objects.filter(codename__in=permission_codename).values_list('pk', flat=True)
        group.permissions.set(permission)

    UserModel = get_user_model()
    user = UserModel.objects.create(username=email, password='testpass')
    organization = Organization.objects.create(
        name=email.split('@')[0],
        phone_number='+0894010101',
        email=email,
        slug=slugify(email.split('@')[0]),
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


def _create_foster_home(email='test_foster_home@gmail.com'):
    foster_home = FosterHome.objects.create(
        phone_number='0894112233',
        email=email,
        cat_available_spots=2,
        dog_available_spots=0,
        bunny_available_spots=0,
        additional_info='',
        location=Point(42.0, 27.0)
    )
    return foster_home


def _create_donation_ticket(organization, category='food', item='Test Food'):
    donation_ticket_data = {
        'category': category,
        'item': item,
        'weight_quantity': 2.0,
        'count_quantity': 0,
        'created_by': organization
    }
    donation_ticket = DonationTickets.objects.create(
        **donation_ticket_data
    )
    donation_ticket.delivery_info.set([_create_delivery_info(organization)])
    return donation_ticket


def _create_delivery_info(organization):
    delivery_address = DonationsDeliveryInfo.objects.create(
        name='Test Name',
        delivery_type='office',
        address='test address',
        phone_number='0894112233',
        additional_info='',
        organization=organization
    )
    return delivery_address


def _instance_dict_no_state(dictionary, keys_to_del=None, keys_to_keep=None):
    if keys_to_del:
        return {k: v for k, v in dictionary.items() if k not in keys_to_del}
    elif keys_to_keep:
        return {k: v for k, v in dictionary.items() if k in keys_to_del}
