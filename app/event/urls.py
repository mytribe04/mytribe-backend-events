from django.urls import path
from . import views

urlpatterns = [
    path("V0.1/event", views.event_list, name = 'event_list'),
    path("V0.1/event/<int:event_id>", views.event_detail, name='event_detail'),
    path("V0.1/organiser", views.organiser_list, name='organiser_list'),
    path("V0.1/organiser/<int:pk>", views.organiser_detail, name="organiser_detail"),
    path("V0.1/sponsor", views.sponsor_list, name="sponsor_list"),
    path("V0.1/sponsor/<int:pk>", views.sponsor_detail, name="sponsor_detail")
]