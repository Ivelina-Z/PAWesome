from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission, Group

from PAWesome.organization.models import Organization


def _create_user_with_organization_profile(permission_codename=None):
    group = Group.objects.create(name='Organizations')
    if permission_codename:
        permission = Permission.objects.get(codename=permission_codename)
        group.permissions.add(permission)

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
