from django.urls import path, include

from PAWesome.organization import views
from PAWesome.organization.views import DashboardView, AddPetView


urlpatterns = (
    # PUBLIC
    path('organizations/', include([
        path('', views.view_all_organizations, name='all-organizations'),
        path('<slug:slug>', views.view_organization, name='organization-details'),
    ])),
    # PRIVATE
    path('organization/<int:pk>/', include([
        path('dashboard/', DashboardView.as_view(), name='dashboard'),
        path('animals/', views.all_animals, name='all-animals'),
        path('add_pet/', AddPetView.as_view(), name='pet-add'),
        path('edit_pet/', views.edit_pet, name='pet-edit')
    ]))
)
