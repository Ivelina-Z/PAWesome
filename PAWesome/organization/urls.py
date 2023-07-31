from django.conf.urls.static import static
from django.urls import path, include

from PAWesome import settings
from PAWesome.organization import views
from PAWesome.organization.views import DashboardView, AllAnimalsView, PendingAdoptForms, DeleteProfile, EditProfile, \
    ViewProfile, HandleAdoptionForm, AllOrganizationsView

urlpatterns = [
    # PUBLIC
    path('organizations/', include([
        path('', AllOrganizationsView.as_view(), name='all-organizations'),
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

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
