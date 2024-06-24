from rest_framework import serializers
from .models import  Event, Sponsor, Organiser
class EventSerializer(serializers.ModelSerializer):
    class Meta :
        model = Event
        fields = ['id', 'event_name', 'event_startdatetime', 'event_enddatetime', 'venue']

class SponsorSerializer(serializers.ModelSerializer):
    sponsor_name = serializers.ReadOnlyField()
    sponsor_email = serializers.ReadOnlyField()
    event_name = serializers.ReadOnlyField()
    event_id = serializers.ReadOnlyField()

    class Meta:
        model = Sponsor
        fields = ['id', 'sponsor_name', 'sponsor_email', 'event_name', 'event_id']

class OrganiserSerializer(serializers.ModelSerializer):
    organiser_name = serializers.ReadOnlyField()
    organiser_email = serializers.ReadOnlyField()
    event_name = serializers.ReadOnlyField()
    event_id = serializers.ReadOnlyField()

    class Meta:
        model = Organiser
        fields = ['id', 'organiser_name', 'organiser_email', 'event_name', 'event_id']