from django.urls import path
from .views import OrganiserView, SponsorView
from .views.EventView import EventAPIView, EventDetailAPIView

urlpatterns = [
    path("V0.1/event", EventAPIView.as_view()),
    path("V0.1/event/<int:event_id>", EventDetailAPIView.as_view()),
    path("V0.1/organiser", OrganiserView.organiser_list, name='organiser_list'),
    path("V0.1/organiser/<int:pk>", OrganiserView.organiser_detail, name="organiser_detail"),
    path("V0.1/sponsor", SponsorView.sponsor_list, name="sponsor_list"),
    path("V0.1/sponsor/<int:pk>", SponsorView.sponsor_detail, name="sponsor_detail")
]
