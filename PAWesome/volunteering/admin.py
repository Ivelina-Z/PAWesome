from django.contrib import admin

from PAWesome.volunteering.models import DonationTickets, DonationsDeliveryInfo, FosterHome


@admin.register(FosterHome)
class FosterHomeAdmin(admin.ModelAdmin):
    pass


@admin.register(DonationTickets)
class FoodDonationTicketsAdmin(admin.ModelAdmin):
    pass


@admin.register(DonationsDeliveryInfo)
class DonationsDeliveryInfoAdmin(admin.ModelAdmin):
    pass
