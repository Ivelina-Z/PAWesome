from django.urls import path, include

from PAWesome.volunteering import views
from PAWesome.volunteering.views import DeliveryInfoView, AddFoodDonation, AddDeliveryInfoView

urlpatterns = (

    path('how-to-help/', include([
        path('', views.how_to_help, name='how-to-help'),
        path('donate/', views.donate, name='donate'),
        path('become-foster-home/', views.add_foster_home, name='foster-home-add')
    ])),
    # PRIVATE
    path('', include([
        path('delivery-info/', DeliveryInfoView.as_view(), name='delivery-info'),
        # path('food-donation/', AddFoodDonation.as_view(), name='food-donation-add'),
    ])),
    path('add/', include([
        path('delivery-info/', AddDeliveryInfoView.as_view(), name='delivery-info-add'),
        path('food-donation/', AddFoodDonation.as_view(), name='food-donation-add'),
        # path('foster-homes/', views.view_foster_homes, name='foster-homes-details'),
    ])),
    # path('delete/', include([
        # path('delivery-info/', DeleteDeliveryInfoView.as_view(), name='delivery-info-delete'),
        # path('food-donation/', DeleteFoodDonation.as_view(), name='food-donation-delete'),
        # path('foster-homes/', views.view_foster_homes, name='foster-homes-details'),
    # ])),
    # path('food-donation/<int:pk>', EditFoodDonationView.as_view(), name='food-donation-edit'),
    # path('food-donation/<int:pk>', DeleteFoodDonationView.as_view(), name='food-donation-delete'),
)
