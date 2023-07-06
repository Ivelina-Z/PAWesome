from django.urls import path

from PAWesome.common.views import IndexView

urlpatterns = (
    path('', IndexView.as_view(), name='homepage'),
)
