from django.contrib.auth.models import User
from django.db import models
from ..utils.model import SoftDeleteModel
from .event import Event


class Sponsor(SoftDeleteModel):
    sponsor = models.ForeignKey(User, on_delete=models.CASCADE)
    events = models.ManyToManyField(Event)


    @property
    def username(self):
        return self.sponsor.username

    @property
    def user_id(self):
        return self.sponsor.id

    @property
    def email(self):
        return self.sponsor.email

    @property
    def sponsored_events(self):
        return [
            {
                "event_id": event.id,
                "event_name": event.event_name
            }
            for event in self.events.all()
        ]

    def __str__(self):
        return self.username

    class Meta:
        app_label = "event"
        db_table = "sponsor"
