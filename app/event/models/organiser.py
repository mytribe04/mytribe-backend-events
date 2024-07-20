from ..utils.model import SoftDeleteModel
from django.db import models
from django.contrib.auth.models import User


class Organiser(SoftDeleteModel):
    organiser = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def username(self):
        return self.organiser.username

    @property
    def user_id(self):
        return self.organiser.id

    @property
    def email(self):
        return self.organiser.email

    @property
    def organised_events(self):
        return [
            {
                "event_name": event.event_name,
                "event_start_datetime": event.event_start_datetime,
                "event_end_datetime": event.event_end_datetime,
                "venue": event.venue
            }
            for event in self.event_set.all()
        ]

    def __str__(self):
        return self.organiser.username

    class Meta:
        app_label = "event"
        db_table = "organiser"
