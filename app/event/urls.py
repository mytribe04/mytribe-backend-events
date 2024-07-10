from django.urls import path
from .views import EventView, OrganiserView, SponsorView

urlpatterns = [
    path("V0.1/event", EventView.event_list, name = 'event_list'),
    path("V0.1/event/<int:event_id>", EventView.event_detail, name='event_detail'),
    path("V0.1/organiser", OrganiserView.organiser_list, name='organiser_list'),
    path("V0.1/organiser/<int:pk>", OrganiserView.organiser_detail, name="organiser_detail"),
    path("V0.1/sponsor", SponsorView.sponsor_list, name="sponsor_list"),
    path("V0.1/sponsor/<int:pk>", SponsorView.sponsor_detail, name="sponsor_detail")
]