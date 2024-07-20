from rest_framework import serializers
from ..models.sponsor import Sponsor


class SponsorSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField()
    email = serializers.ReadOnlyField()
    sponsored_events = serializers.ReadOnlyField()

    class Meta:
        model = Sponsor
        fields = [
            'id',
            'username',
            'email',
            'sponsored_events'
        ]