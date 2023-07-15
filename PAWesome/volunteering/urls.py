from django.urls import path, include

from PAWesome.volunteering import views
from PAWesome.volunteering.views import DeliveryInfoView, AddDonationTicket, AddDeliveryInfoView, EditDeliveryInfoView, \
    EditDonationTickets, FoodDonationView, AddFosterHome, FosterHomes, DeleteDeliveryInfoView, DeleteDonationTicket, \
    EditFosterHome, DeleteFosterHome

urlpatterns = (
    path('how-to-help/', include([
        path('', views.how_to_help, name='how-to-help'),
        path('become-foster-home/', AddFosterHome.as_view(), name='foster-home-add')
    ])),
    # PRIVATE
    path('', include([
        path('delivery-info/', DeliveryInfoView.as_view(), name='delivery-info'),
        path('donation-tickets/', FoodDonationView.as_view(), name='donation-ticket'),
        path('foster-homes/', FosterHomes.as_view(), name='foster-homes')
    ])),
    path('add/', include([
        path('delivery-info/', AddDeliveryInfoView.as_view(), name='delivery-info-add'),
        path('donation-tickets/', AddDonationTicket.as_view(), name='donation-ticket-add'),
    ])),
    path('edit/', include([
        path('delivery-info/<int:pk>/', EditDeliveryInfoView.as_view(), name='delivery-info-edit'),
        path('donation-tickets/<int:pk>/', EditDonationTickets.as_view(), name='donation-ticket-edit'),
        path('foster-home/<token>/', EditFosterHome.as_view(), name='foster-home-edit')
    ])),
    path('delete/', include([
        path('delivery-info/<int:pk>/', DeleteDeliveryInfoView.as_view(), name='delivery-info-delete'),
        path('donation-tickets/<int:pk>/', DeleteDonationTicket.as_view(), name='donation-ticket-delete'),
        path('foster-home/<token>/', DeleteFosterHome.as_view(), name='foster-home-delete')
    ]))
)
