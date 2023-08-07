from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase, Client
from django.urls import reverse

from PAWesome.volunteering.models import DonationTickets
from PAWesome.volunteering.views import AddDonationTicket
from tests.setup import _create_user_with_organization_profile, _create_delivery_info, _instance_dict_no_state


class TestAddDonationTicket(TestCase):
    def setUp(self):
        self.user, self.organization, _ = _create_user_with_organization_profile()
        self.delivery_info = _create_delivery_info(self.organization)

        self.url = reverse('donation-ticket-add')
        self.client = Client()

    def test__add_donation_ticket_unauthorized_user__should_redirect_to_login(self):
        response = self.client.get(self.url)

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('login') + f'?next={self.url}')

    def test__add_donation_ticket_authorized_user__should_render(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, AddDonationTicket.template_name)

    def test__add_donation_ticket_valid_form_data__should_create_object(self):
        self.client.force_login(self.user)

        valid_form_data = {
            'category': 'food',
            'item': 'Test Food',
            'weight_quantity': 2.0,
            'count_quantity': 0,
            'delivery_info': [self.delivery_info.pk]
        }
        response = self.client.post(self.url, valid_form_data)

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse(
            'dashboard',
            kwargs={'slug': self.organization.slug}
        ))

        self.assertTrue(DonationTickets.objects.filter(item=valid_form_data['item']).exists())
        new_donation_ticket = DonationTickets.objects.get(item=valid_form_data['item'])
        new_donation_ticket_data = _instance_dict_no_state(
            new_donation_ticket.__dict__,
            keys_to_del=['_state', 'id', 'created_by_id', 'date_of_publication']
        )
        valid_form_data.pop('delivery_info')
        self.assertEquals(new_donation_ticket_data, valid_form_data)

    def test__add_donation_ticket_invalid_form_data__should_render_form_with_errors(self):
        self.client.force_login(self.user)

        invalid_form_data = {
            'category': 'invalid',
            'item': 'Test Food',
            'weight_quantity': 2.0,
            'count_quantity': 0,
            'delivery_info': [self.delivery_info.pk]
        }
        response = self.client.post(self.url, invalid_form_data)

        self.assertEquals(response.status_code, 200)
        form = response.context['form']
        self.assertEquals(len(form.errors), 1)

        self.assertEquals(
            form.errors['category'],
            ['Select a valid choice. invalid is not one of the available choices.']
        )

        with self.assertRaises(ObjectDoesNotExist) as e:
            DonationTickets.objects.get(item=invalid_form_data['item'])
