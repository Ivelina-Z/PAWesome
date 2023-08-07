from django.test import TestCase, Client
from django.urls import reverse

from PAWesome.volunteering.models import DonationTickets
from PAWesome.volunteering.views import EditDonationTickets
from tests.setup import _create_user_with_organization_profile, _create_delivery_info, _instance_dict_no_state, \
    _create_donation_ticket


class TestEditDonationTicket(TestCase):
    def setUp(self):
        self.user, self.organization, _ = _create_user_with_organization_profile()
        self.delivery_info = _create_delivery_info(self.organization)
        self.donation_ticket = _create_donation_ticket(self.organization)

        self.valid_updated_form_data = {
            'category': 'food',
            'item': 'Test Food',
            'weight_quantity': 3.0,
            'count_quantity': 0,
            'delivery_info': [self.delivery_info.pk]
        }

        self.url = reverse(
            'donation-ticket-edit',
            kwargs={'pk': self.donation_ticket.pk}
        )
        self.client = Client()

    def test__edit_donation_ticket_unauthorized_user__should_redirect_to_login(self):
        response = self.client.get(self.url)

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('login') + f'?next={self.url}')

    def test__edit_donation_ticket_authorized_user__should_render(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, EditDonationTickets.template_name)

    def test__edit_donation_ticket_valid_form_data__should_update_object(self):
        self.client.force_login(self.user)

        response = self.client.post(self.url, self.valid_updated_form_data)

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse(
            'dashboard',
            kwargs={'slug': self.organization.slug}
        ))

        updated_donation_ticket = DonationTickets.objects.get(pk=self.donation_ticket.pk)
        self.assertEquals(updated_donation_ticket.pk, self.donation_ticket.pk)
        self.assertEquals(updated_donation_ticket.weight_quantity, self.valid_updated_form_data['weight_quantity'])

    def test__edit_donation_ticket_invalid_form_data__should_render_form_with_errors(self):
        self.client.force_login(self.user)
        invalid_updated_form_data = self.valid_updated_form_data.copy()
        invalid_updated_form_data['category'] = 'invalid'

        response = self.client.post(self.url, invalid_updated_form_data)

        self.assertEquals(response.status_code, 200)

        form = response.context['form']
        self.assertEquals(
            form.errors['category'],
            ['Select a valid choice. invalid is not one of the available choices.']
        )

        self.assertEquals(
            DonationTickets.objects.get(item=invalid_updated_form_data['item']).category,
            self.valid_updated_form_data['category']
        )
