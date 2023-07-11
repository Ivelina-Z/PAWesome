from django.contrib import admin

from PAWesome.volunteering.models import FoodDonationTickets, DonationsDeliveryInfo


@admin.register(FoodDonationTickets)
class FoodDonationTicketsAdmin(admin.ModelAdmin):
    pass


@admin.register(DonationsDeliveryInfo)
class DonationsDeliveryInfoAdmin(admin.ModelAdmin):
    pass
