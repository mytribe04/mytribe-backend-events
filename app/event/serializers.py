from rest_framework import serializers
from .models import  Event, Sponsor, Organiser


class EventSerializer(serializers.ModelSerializer):
    organisers_details = serializers.ReadOnlyField()
    sponsors_details = serializers.ReadOnlyField()

    class Meta:
        model = Event
        fields = [
            'id', 'event_name', 'event_start_datetime',
            'event_end_datetime', 'venue', 'organisers_details',
            'sponsors_details'
        ]


class SponsorSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField()
    email = serializers.ReadOnlyField()
    sponsored_events = serializers.ReadOnlyField()

    class Meta:
        model = Sponsor
        fields = ['id', 'username', 'email', 'sponsored_events']


class OrganiserSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField()
    email = serializers.ReadOnlyField()
    organised_events = serializers.ReadOnlyField()

    class Meta:
        model = Organiser
        fields = ['id', 'username', 'email', 'organised_events']