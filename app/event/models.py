from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Event(models.Model):
    event_name = models.CharField(max_length = 200)
    event_startdatetime = models.DateTimeField()
    event_enddatetime = models.DateTimeField()
    venue = models.CharField(max_length=200, default="---- event location ----")



class Sponsor(models.Model):
    sponsor = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    @property
    def sponsor_name(self):
        return self.sponsor.username

    @property
    def sponsor_email(self):
        return self.sponsor.email


    @property
    def event_name(self):
        return self.event.name

    @property
    def event_id(self):
        return self.event_id
class Organiser(models.Model):
    organiser = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    @property
    def organiser_name(self):
        return self.organiser.username

    @property
    def organiser_email(self):
        return self.organiser.email

    @property
    def event_name(self):
        return self.event.name

    @property
    def event_id(self):
        return self.event_id
