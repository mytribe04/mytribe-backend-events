from rest_framework import serializers
from ..models.event import Event


class EventSerializer(serializers.ModelSerializer):
    organisers_details = serializers.ReadOnlyField()
    sponsors_details = serializers.ReadOnlyField()

    class Meta:
        model = Event
        fields = [
            'id',
            'event_name',
            'event_start_datetime',
            'event_end_datetime',
            'venue',
            'organisers_details',
            'sponsors_details'
        ]