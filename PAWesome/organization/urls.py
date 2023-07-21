from django.conf.urls.static import static
from django.urls import path, include

from PAWesome import settings
from PAWesome.organization import views
from PAWesome.organization.views import DashboardView, AddAnimalView, AllAnimalsView, EditAnimalView, \
    DeleteAnimalView, PendingAdoptForms, HandleAdoptionForm, DeleteProfile, EditProfile, ViewProfile

urlpatterns = [
    # PUBLIC
    path('organizations/', include([
        path('', views.view_all_organizations, name='all-organizations'),
        path('<slug:slug>', views.view_organization, name='organization-details'),
    ])),
    # PRIVATE
    path('organization/<slug:slug>/', include([
        path('dashboard/', DashboardView.as_view(), name='dashboard'),
        path('animals/', AllAnimalsView.as_view(), name='organization-animals'),
        path('for-approval/', PendingAdoptForms.as_view(), name='organization-pending-adoption-forms'),
        path('for-approval/<int:pk>/', HandleAdoptionForm.as_view(), name='organization-handle-adoption-forms'),
    ])),
    path('profile/', include([
        path('edit/<int:pk>', EditProfile.as_view(), name='profile-edit'),
        path('delete/<int:pk>', DeleteProfile.as_view(), name='profile-delete'),
        path('view/<int:pk>', ViewProfile.as_view(), name='profile-view'),
    ])),
    path('add/animal/', AddAnimalView.as_view(), name='animal-add'),
    path('edit/animal/<int:pk>', EditAnimalView.as_view(), name='animal-edit'),
    path('delete/animal/<int:pk>', DeleteAnimalView.as_view(), name='animal-delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
