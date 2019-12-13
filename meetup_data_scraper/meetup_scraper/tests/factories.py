from typing import Any, Sequence
from factory import DjangoModelFactory, Faker, post_generation
from django.utils import timezone
from datetime import datetime, timedelta
import pytz
import pytest

timezone.activate(pytz.timezone("UTC"))

meetup_groups: dict = {
    "sandbox": {"meetup_id": 1556336, "urlname": "Meetup-API-Testing"},
    "not-exist": {"meetup_id": 123456, "urlname": "None"},
    "gone": {"meetup_id": 654321, "urlname": "connectedawareness-berlin"},
}


class EventPage1Factory(DjangoModelFactory):
    class Meta:
        model = "meetup_scraper.EventPage"
        django_get_or_create = [
            "meetup_id",
        ]

    # custom models
    meetup_id = "11947605"
    attendance_count = 10
    attendance_sample = 10
    attendee_sample = 10
    created = timezone.make_aware(datetime.strptime("2009-11-13", "%Y-%m-%d"))
    description = "BUH"
    duration = timedelta(seconds=960)
    fee_accepts = "cash"
    fee_amount = 1
    fee_currency = "EUR"
    fee_description = "DESCRIPTION"
    fee_label = "LABEL"
    how_to_find_us = "how_to_find_us"
    how_to_find_us = "how_to_find_us"
    name = "test meetup"
    status = "past"
    time = timezone.make_aware(datetime.strptime("2014-01-15", "%Y-%m-%d"))
    updated = timezone.make_aware(datetime.strptime("2014-01-15", "%Y-%m-%d"))
    utc_offset = 0
    venue_visibility = "public"
    visibility = "public"

    # wagtail models
    title = "{}: {}".format(meetup_id, name)
    slug = meetup_id
    path = "0001000100019001"
    depth = 4


class EventPage2Factory(EventPage1Factory):
    meetup_id = "15467880"
    time = timezone.make_aware(datetime.strptime("2015-01-15", "%Y-%m-%d"))
    path = "0001000100019002"


class EventPage3Factory(EventPage1Factory):
    meetup_id = "13041272"
    time = timezone.make_aware(datetime.strptime("2011-01-15", "%Y-%m-%d"))
    path = "0001000100019003"


class GroupPageFactory(DjangoModelFactory):
    class Meta:
        model = "meetup_scraper.GroupPage"
        django_get_or_create = [
            "urlname",
        ]

    # custom models
    meetup_id = meetup_groups["sandbox"]["meetup_id"]
    name = "Meetup API Testing Sandbox"
    status = "active"
    urlname = meetup_groups["sandbox"]["urlname"]
    description = "<p>the Meetup Testing group</p>"
    created = timezone.make_aware(datetime.strptime("2009-11-13", "%Y-%m-%d"))
    city = "Brooklyn"
    country = "US"
    lat = 40.7
    lon = -73.99
    link = "https://localhost/"
    members = 10
    status = "aktive"
    timezone = "Europe/Berlin"
    visibility = "public"

    # wagtail models
    title = "{}: {}".format(meetup_id, name)
    slug = meetup_id
    path = "000100010001"
    depth = 3


class NotExistGroupPageFactory(GroupPageFactory):
    # custom models
    meetup_id = meetup_groups["not-exist"]["meetup_id"]

    # wagtail models
    title = meetup_id
    slug = meetup_id
    urlname = meetup_groups["not-exist"]["urlname"]
    path = "000100010002"


class ImprintPageFactory(DjangoModelFactory):
    class Meta:
        model = "meetup_scraper.SimplePage"
        django_get_or_create = [
            "title",
        ]

    # custom models
    body = "<p>HTML content</p>"

    # wagtail models
    title = "Imprint"
    slug = title
    path = "000100010003"
    depth = 3

class PrivacyPageFactory(DjangoModelFactory):
    # wagtail models
    title = "Privacy"
    slug = title
    path = "000100010004"