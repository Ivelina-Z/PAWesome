from django.test import TestCase, Client
from django.urls import reverse

from PAWesome.volunteering.models import DonationTickets
from PAWesome.volunteering.views import ListDonationView
from tests.setup import _create_user_with_organization_profile, _create_donation_ticket


class TestListDonation(TestCase):
    def setUp(self):
        self.user, self.organization, _ = _create_user_with_organization_profile()
        self.donation_ticket_1 = _create_donation_ticket(self.organization)
        self.donation_ticket_2 = _create_donation_ticket(self.organization)

        _, self.other_organization, _ = _create_user_with_organization_profile(email='testuser2@gmail.com')
        self.donation_ticket_3_other_organization = _create_donation_ticket(self.other_organization)

        self.test_medication_donation_ticket = _create_donation_ticket(
            self.organization,
            category='medications',
            item='Test Medication'
        )

        self.query_string = {'category': 'medications'}
        self.url = reverse('donation-tickets')
        self.client = Client()

    def test__list_donation_tickets_public__should_list_all_tickets(self):
        response = self.client.get(self.url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, ListDonationView.template_name)

    def test__list_donation_tickets_private__should_list_only_organizations_tickets(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, ListDonationView.template_name)
        self.assertQuerysetEqual(
            response.context['object_list'],
            [self.donation_ticket_1, self.donation_ticket_2, self.test_medication_donation_ticket],
            ordered=False
        )

    def test__filter_by_category_medications__should_show_only_medications(self):
        response = self.client.get(self.url, self.query_string)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, ListDonationView.template_name)
        self.assertQuerysetEqual(
            response.context['object_list'],
            [self.test_medication_donation_ticket]
        )

    def test__filter_by_category_authorized_user__should_return_only_users_tickets_filtered(self):
        self.client.force_login(self.user)

        test_medication_donation_ticket_other_organization = _create_donation_ticket(
            self.other_organization,
            category='medications',
            item='Test Medication 2'
        )

        response = self.client.get(self.url, self.query_string)
        self.assertEquals(response.status_code, 200)

        self.assertEquals(
            len(DonationTickets.objects.filter(category='medications')),
            2
        )
        self.assertQuerysetEqual(
            response.context['object_list'],
            [self.test_medication_donation_ticket]
        )
