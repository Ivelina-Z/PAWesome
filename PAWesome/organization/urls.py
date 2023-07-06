from django.urls import path, include

from PAWesome.organization import views
# from PAWesome.organization.views import RegisterOrganizationView

urlpatterns = (
    # PUBLIC
    path('organizations/', include([
        path('', views.view_all_organizations, name='all-organizations'),
        path('<slug:slug>', views.view_organization, name='organization-details'),
    ])),
    # PRIVATE
    path('organization/<slug:slug>', include([
        path('dashboard/', views.dashboard, name='dashboard'),
        path('animals/', views.all_animals, name='all-animals'),
        path('add_pet/', views.add_pet, name='pet-add'),
        path('edit_pet/', views.edit_pet, name='pet-edit')
    ]))
)

