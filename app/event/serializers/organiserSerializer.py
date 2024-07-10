from rest_framework import serializers
from ..models.organiser import Organiser


class OrganiserSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField()
    email = serializers.ReadOnlyField()
    organised_events = serializers.ReadOnlyField()

    class Meta:
        model = Organiser
        fields = ['id', 'username', 'email', 'organised_events']