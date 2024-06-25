from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Organiser(models.Model):
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


class Event(models.Model):
    event_name = models.CharField(max_length = 200)
    event_start_datetime = models.DateTimeField()
    event_end_datetime = models.DateTimeField()
    venue = models.CharField(max_length=200, default="---- event location ----")
    organisers = models.ManyToManyField(Organiser)

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


class Sponsor(models.Model):
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


