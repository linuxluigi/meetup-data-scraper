from typing import Any, Sequence
from factory import DjangoModelFactory, Faker, post_generation
from django.utils import timezone
from datetime import datetime
import pytz

timezone.activate(pytz.timezone("UTC"))

sandbox_meetup_group: dict = {"meetup_id": 1556336, "urlname": "Meetup-API-Testing"}


class GroupPageFactory(DjangoModelFactory):
    class Meta:
        model = "meetup_scraper.GroupPage"
        django_get_or_create = [
            "urlname",
        ]

    # custom models
    meetup_id = sandbox_meetup_group["meetup_id"]
    name = "Meetup API Testing Sandbox"
    status = "active"
    urlname = sandbox_meetup_group["urlname"]
    description = " "
    created = timezone.make_aware(datetime.strptime("2009-11-13", "%Y-%m-%d"))
    city = "Brooklyn"
    country = "US"
    lat = 40.7
    lon = -73.99
    members = 10

    # wagtail models
    title = "{}: {}".format(meetup_id, name)
    slug = meetup_id
    path = "000100010001"
    depth = 3


class EventPage1Factory(DjangoModelFactory):
    class Meta:
        model = "meetup_scraper.EventPage"
        django_get_or_create = [
            "meetup_id",
        ]

    # custom models
    meetup_id = "11947605"
    name = "test meetup"
    time = timezone.make_aware(datetime.strptime("2014-01-15", "%Y-%m-%d"))

    # wagtail models
    title = "{}: {}".format(meetup_id, name)
    slug = meetup_id
    path = "0001000100010001"
    depth = 4


class EventPage2Factory(EventPage1Factory):
    meetup_id = "15467880"
    time = timezone.make_aware(datetime.strptime("2015-01-15", "%Y-%m-%d"))
    path = "0001000100010002"


class EventPage3Factory(EventPage1Factory):
    meetup_id = "13041272"
    time = timezone.make_aware(datetime.strptime("2011-01-15", "%Y-%m-%d"))
    path = "0001000100010003"
