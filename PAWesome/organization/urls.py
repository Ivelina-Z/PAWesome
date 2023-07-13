from django.urls import path, include

from PAWesome.organization import views
from PAWesome.organization.views import DashboardView, AddAnimalView, AllAnimalsView, EditAnimalView, \
    DeleteAnimalView, AllWaitingForApproval, WaitingForApprovalDetails, FoodDonationView

urlpatterns = (
    # PUBLIC
    path('organizations/', include([
        path('', views.view_all_organizations, name='all-organizations'),
        path('<slug:slug>', views.view_organization, name='organization-details'),
    ])),
    # PRIVATE
    path('organization/<slug:slug>/', include([
        path('dashboard/', DashboardView.as_view(), name='dashboard'),
        path('animals/', AllAnimalsView.as_view(), name='organization-animals'),
        path('for-approval/', AllWaitingForApproval.as_view(), name='organization-waiting-for-approval'),
        path('for-approval/<int:animal_pk>', WaitingForApprovalDetails.as_view(), name='organization-waiting-for-approval-details'),
        # path('food-donation/', FoodDonationView.as_view(), name='organization-food-donation')
    ])),
    path('add/animal/', AddAnimalView.as_view(), name='animal-add'),
    path('edit/animal/<int:pk>', EditAnimalView.as_view(), name='animal-edit'),
    path('delete/animal/<int:pk>', DeleteAnimalView.as_view(), name='animal-delete'),
    # path('adopted/<int:pk>', AdoptedPetView.as_view(), name='pet-adopted'),
)
