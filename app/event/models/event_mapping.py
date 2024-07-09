from django.contrib.postgres.fields import ArrayField
from django.db import models

from ..utils.model import SoftDeleteModel


class EventMapping(SoftDeleteModel):
    event_id = models.ForeignKey(to="Event", null=False, on_delete=models.DO_NOTHING)
    remote_sponsor_ids = ArrayField(
        null=True,
        blank=True,
        base_field=models.BigIntegerField(null=True, blank=True),
    )
    organizing_team = ArrayField(
        null=True,
        blank=True,
        base_field=models.BigIntegerField(null=True, blank=True),
    )

    class Meta:
        app_label = "event_mapping"
        db_table = "event_mapping"
