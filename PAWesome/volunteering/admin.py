from django.contrib import admin
from django.contrib.gis import admin as gis_admin

from PAWesome.volunteering.forms import FosterHomeForm, DonationForm
from PAWesome.volunteering.models import DonationTickets, DonationsDeliveryInfo, FosterHome


@admin.register(FosterHome)
class FosterHomeAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'cat_available_spots', 'dog_available_spots', 'bunny_available_spots')
    exclude = []

    def get_exclude(self, request, obj=None):
        exclude_fields = super().get_exclude(request, obj)
        if not request.user.is_superuser:
            exclude_fields.append('token')
        return exclude_fields


@admin.register(DonationTickets)
class DonationTicketsAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'category')
    list_filter = ('category', )
    search_fields = ('item', )
    exclude = []

    def get_exclude(self, request, obj=None):
        exclude_fields = super().get_exclude(request, obj)
        if not request.user.is_superuser:
            exclude_fields.append('created_by')
        return exclude_fields

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "delivery_info" and not request.user.is_superuser:
            kwargs["queryset"] = DonationsDeliveryInfo.objects.filter(organization=request.user.organization)
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            if not change:
                obj.created_by = request.user.organization
        return super().save_model(request, obj, form, change)


@admin.register(DonationsDeliveryInfo)
class DonationsDeliveryInfoAdmin(admin.ModelAdmin):
    pass
