from django.urls import path, include

from PAWesome.organization import views
from PAWesome.organization.views import DashboardView, AddPetView, AllAnimalsView, EditPetView, DeletePetView

urlpatterns = (
    # PUBLIC
    path('organizations/', include([
        path('', views.view_all_organizations, name='all-organizations'),
        path('<slug:slug>', views.view_organization, name='organization-details'),
    ])),
    # PRIVATE
    path('organization/<int:pk>/', include([
        path('dashboard/', DashboardView.as_view(), name='dashboard'),
        path('animals/', AllAnimalsView.as_view(), name='organization-animals')])),
    path('add_pet/', AddPetView.as_view(), name='pet-add'),
    path('edit_pet/<int:pk>', EditPetView.as_view(), name='pet-edit'),
    path('delete_pet/<int:pk>', DeletePetView.as_view(), name='pet-delete'),
    # path('adopted/<int:pk>', AdoptedPetView.as_view(), name='pet-adopted'),
)
