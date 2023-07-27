from django.contrib import admin

from PAWesome.volunteering.models import DonationTickets, DonationsDeliveryInfo, FosterHome


@admin.register(FosterHome)
class FosterHomeAdmin(admin.ModelAdmin):
    pass


@admin.register(DonationTickets)
class DonationTicketsAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'category')
    list_filter = ('category', )
    search_fields = ('item', )


@admin.register(DonationsDeliveryInfo)
class DonationsDeliveryInfoAdmin(admin.ModelAdmin):
    pass
