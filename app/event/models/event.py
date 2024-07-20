from django.db import models

from ..utils.field import IntegerChoiceField
from ..utils.model import SoftDeleteModel
from .organiser import Organiser


class Event(SoftDeleteModel):
    organisers = models.ManyToManyField(Organiser)
    event_name = models.CharField(max_length=200)
    event_start_datetime = models.DateTimeField()
    event_end_datetime = models.DateTimeField()
    venue = models.CharField(max_length=200, default="---- event location ----")

    @property
    def organisers_details(self):
        return [
            {"organiser_username": organiser_obj.username,
             "organiser_email": organiser_obj.email}
            for organiser_obj in self.organisers.all()]

    @property
    def sponsors_details(self):
        return [
            {
                "sponsor_username": sponsor.username,
                "sponsor_email": sponsor.email
            }
            for sponsor in self.sponsor_set.all()
        ]

    def __str__(self):
        return self.event_name

    class Meta:
        app_label = "event"
        db_table = "event"
