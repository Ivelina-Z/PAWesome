from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase, Client
from django.urls import reverse

from PAWesome.volunteering.models import DonationTickets
from PAWesome.volunteering.views import DeleteDonationTicket
from tests.setup import _create_user_with_organization_profile, _create_delivery_info, \
    _create_donation_ticket


class TestDeleteDonationTickets(TestCase):
    def setUp(self):
        self.user, self.organization, self.group = _create_user_with_organization_profile(
            ['delete_donationtickets']
        )
        self.delivery_info = _create_delivery_info(self.organization)
        self.donation_ticket = _create_donation_ticket(self.organization)

        self.url = reverse(
            'donation-ticket-delete',
            kwargs={'pk': self.donation_ticket.pk})
        self.client = Client()

    def test__delete_donation_ticket_unauthorized_user__should_redirect_to_login(self):
        response = self.client.get(self.url)

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('login') + f'?next={self.url}')

    def test__delete_donation_ticket_no_permissions__should_return_403(self):
        self.user.groups.remove(self.group)
        self.client.force_login(self.user)
        response = self.client.get(self.url)

        self.assertEquals(response.status_code, 403)

    def test__delete_donation_ticket_authorized_user__should_render(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, DeleteDonationTicket.template_name)

    def test__delete_donation_ticket__should_delete(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url)

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, DeleteDonationTicket.success_url)

        with self.assertRaises(ObjectDoesNotExist) as e:
            DonationTickets.objects.get(pk=self.donation_ticket.pk)
