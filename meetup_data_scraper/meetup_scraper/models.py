from django.db import models

from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.search import index
from wagtail.api import APIField


class HomePage(Page):
    """
    Default Home Page
    """

    subpage_types = ["meetup_scraper.GroupPage"]  # allowd child page types


class EventPage(Page):
    """
    Meetup Event
    """

    # models
    meetup_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=100, blank=True, null=True)
    time = models.DateTimeField()
    description = models.TextField(blank=True, null=True)

    # admin interface panels
    content_panels = Page.content_panels + [
        FieldPanel("meetup_id"),
        FieldPanel("name"),
        FieldPanel("status"),
        FieldPanel("time"),
        FieldPanel("description"),
    ]

    # Search index configuration
    search_fields = Page.search_fields + [
        index.SearchField("meetup_id"),
        index.SearchField("name"),
        index.SearchField("status"),
        index.SearchField("time"),
        index.FilterField("description"),
    ]

    # api fields
    api_fields = [
        APIField("meetup_id"),
        APIField("name"),
        APIField("status"),
        APIField("time"),
        APIField("description"),
    ]

    parent_page_types = ["meetup_scraper.GroupPage"]  # allowd parent page types
    subpage_types = []  # no child pages allowed


class GroupPage(Page):
    """
    Meetup Event
    """

    # models
    meetup_id = models.BigIntegerField(unique=True)
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    urlname = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    created = models.DateTimeField()
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=5)
    lat = models.DecimalField(max_digits=10, decimal_places=8)
    lon = models.DecimalField(max_digits=10, decimal_places=8)
    members = models.IntegerField()

    # admin interface panels
    content_panels = Page.content_panels + [
        FieldPanel("meetup_id"),
        FieldPanel("name"),
        FieldPanel("status"),
        FieldPanel("urlname"),
        FieldPanel("description"),
        FieldPanel("created"),
        FieldPanel("city"),
        FieldPanel("country"),
        FieldPanel("lat"),
        FieldPanel("lon"),
        FieldPanel("members"),
    ]

    # Search index configuration
    search_fields = Page.search_fields + [
        index.SearchField("meetup_id"),
        index.SearchField("name"),
        index.SearchField("status"),
        index.SearchField("urlname"),
        index.SearchField("description"),
        index.FilterField("created"),
        index.FilterField("city"),
        index.FilterField("country"),
        index.FilterField("lat"),
        index.FilterField("lon"),
        index.FilterField("members"),
    ]

    # api fields
    api_fields = [
        APIField("meetup_id"),
        APIField("name"),
        APIField("status"),
        APIField("urlname"),
        APIField("description"),
        APIField("created"),
        APIField("city"),
        APIField("country"),
        APIField("lat"),
        APIField("lon"),
        APIField("members"),
    ]

    parent_page_types = ["meetup_scraper.HomePage"]  # allowd parent page types
    subpage_types = ["meetup_scraper.EventPage"]  # allowd child page types

    def events(self) -> [EventPage]:
        """
        get all events from the database ordered by time des

        return -> [EventPage]
        """

        # Get list of live event pages that are descendants of this page
        events: [EventPage] = EventPage.objects.live().descendant_of(self)

        # Order by date
        return events.order_by("-time")

    def last_event(self) -> EventPage:
        """
        get last event of the group

        return -> EventPage when there is an event else None
        """

        try:
            return self.events()[:1].get()
        except EventPage.DoesNotExist:
            return None
