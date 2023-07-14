from django.urls import path, include

from PAWesome.volunteering import views
from PAWesome.volunteering.views import DeliveryInfoView, AddDonationTicket, AddDeliveryInfoView, EditDeliveryInfoView, \
    EditDonationTickets, FoodDonationView, AddFosterHome, FosterHomes, DeleteDeliveryInfoView

urlpatterns = (
    path('how-to-help/', include([
        path('', views.how_to_help, name='how-to-help'),
        path('become-foster-home/', AddFosterHome.as_view(), name='foster-home-add')
    ])),
    # PRIVATE
    path('', include([
        path('delivery-info/', DeliveryInfoView.as_view(), name='delivery-info'),
        path('food-donation/', FoodDonationView.as_view(), name='food-donation'),
        path('foster-homes/', FosterHomes.as_view(), name='foster-homes')
    ])),
    path('add/', include([
        path('delivery-info/', AddDeliveryInfoView.as_view(), name='delivery-info-add'),
        path('food-donation/', AddDonationTicket.as_view(), name='food-donation-add'),
    ])),
    path('edit/', include([
        path('delivery-info/<int:pk>/', EditDeliveryInfoView.as_view(), name='delivery-info-edit'),
        path('food-donation/<int:pk>/', EditDonationTickets.as_view(), name='food-donation-edit'),
    ])),
    path('delete/', include([
        path('delivery-info/<int:pk>/', DeleteDeliveryInfoView.as_view(), name='delivery-info-delete'),
        # path('food-donation/<int:pk>/', DeleteFoodDonation.as_view(), name='food-donation-delete'),
        # path('foster-homes/<int:pk>/', views.view_foster_homes, name='foster-homes-details'),
    ]))
)
