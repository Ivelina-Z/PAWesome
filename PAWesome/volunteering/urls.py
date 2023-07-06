from django.urls import path, include

from PAWesome.volunteering import views

urlpatterns = (

    path('how-to-help/', include([
        path('', views.how_to_help, name='how-to-help'),
        path('donate/', views.donate, name='donate'),
        path('become-foster-home/', views.add_foster_home, name='foster-home-add')
    ])),
    # PRIVATE
    path('foster-homes/', views.view_foster_homes, name='foster-homes-details')
)
