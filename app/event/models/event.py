from django.db import models

from ..utils.field import IntegerChoiceField
from ..utils.model import SoftDeleteModel


class Event(SoftDeleteModel):
    remote_organizer_id = models.BigIntegerField(null=True, blank=True)
    event_name = models.CharField(max_length=200)
    event_start_datetime = models.DateTimeField()
    event_end_datetime = models.DateTimeField()
    venue = models.CharField(max_length=200, default="---- event location ----")

    class Meta:
        app_label = "event"
        db_table = "event"
