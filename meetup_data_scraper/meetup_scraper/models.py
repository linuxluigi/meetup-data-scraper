from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel
from wagtail.search import index
from wagtail.api import APIField
from modelcluster.fields import ParentalKey
from wagtail.snippets.models import register_snippet
from django.forms.models import model_to_dict


class SimplePage(Page):

    body = RichTextField()

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    parent_page_types = ["meetup_scraper.HomePage"]  # allow parent page types
    subpage_types = []  # allow child page types


class HomePage(Page):
    """
    Default Home Page
    """

    @property
    def child_pages(self):
        simple_pages: [SimplePage] = SimplePage.objects.live().child_of(self)

        if not simple_pages.exists():
            return []

        pages: [dict] = []
        for page in simple_pages:
            pages.append(model_to_dict(page))

        return pages

    # api fields
    api_fields = [
        APIField("child_pages"),
    ]

    subpage_types = [
        "meetup_scraper.GroupPage",
        "meetup_scraper.SimplePage",
    ]  # allow child page types


@register_snippet
class Photo(models.Model):
    """
    Meetup Photo
    """

    meetup_id = models.BigIntegerField(unique=True)
    highres_link = models.URLField(blank=True, null=True)
    photo_link = models.URLField(blank=True, null=True)
    thumb_link = models.URLField(blank=True, null=True)
    photo_type = models.CharField(max_length=50, blank=True, null=True)
    base_url = models.URLField(blank=True, null=True)

    # admin interface panels
    panels = [
        FieldPanel("meetup_id"),
        FieldPanel("highres_link"),
        FieldPanel("photo_link"),
        FieldPanel("thumb_link"),
        FieldPanel("photo_type"),
        FieldPanel("base_url"),
    ]

    # Search index configuration
    search_fields = Page.search_fields + [
        index.SearchField("meetup_id"),
        index.SearchField("highres_link"),
        index.SearchField("photo_link"),
        index.SearchField("thumb_link"),
        index.SearchField("photo_type"),
        index.SearchField("base_url"),
    ]

    # api fields
    api_fields = [
        APIField("meetup_id"),
        APIField("highres_link"),
        APIField("photo_link"),
        APIField("thumb_link"),
        APIField("photo_type"),
        APIField("base_url"),
    ]


@register_snippet
class Member(models.Model):
    meetup_id = models.BigIntegerField(unique=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    photo = models.ForeignKey(Photo, on_delete=models.SET_NULL, blank=True, null=True)

    # admin interface panels
    panels = [
        FieldPanel("meetup_id"),
        FieldPanel("name"),
        FieldPanel("bio"),
        FieldPanel("photo"),
    ]

    # Search index configuration
    search_fields = Page.search_fields + [
        index.SearchField("meetup_id"),
        index.SearchField("name"),
        index.SearchField("bio"),
        index.SearchField("photo"),
    ]

    # api fields
    api_fields = [
        APIField("meetup_id"),
        APIField("name"),
        APIField("bio"),
        APIField("photo"),
    ]


@register_snippet
class Venue(models.Model):
    """
    Meetup Venue
    """

    meetup_id = models.IntegerField(unique=True)
    address_1 = models.CharField(max_length=255, blank=True, null=True)
    address_2 = models.CharField(max_length=255, blank=True, null=True)
    address_3 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    lat = models.DecimalField(max_digits=40, decimal_places=30, blank=True, null=True)
    lon = models.DecimalField(max_digits=40, decimal_places=30, blank=True, null=True)
    localized_country_name = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    zip_code = models.CharField(max_length=255, blank=True, null=True)

    # admin interface panels
    panels = [
        FieldPanel("meetup_id"),
        FieldPanel("name"),
        FieldPanel("address_1"),
        FieldPanel("address_2"),
        FieldPanel("address_3"),
        FieldPanel("city"),
        FieldPanel("zip_code"),
        FieldPanel("country"),
        FieldPanel("lat"),
        FieldPanel("lon"),
        FieldPanel("localized_country_name"),
        FieldPanel("phone"),
    ]

    # Search index configuration
    search_fields = Page.search_fields + [
        index.SearchField("meetup_id"),
        index.SearchField("address_1"),
        index.SearchField("address_2"),
        index.SearchField("address_3"),
        index.SearchField("city"),
        index.SearchField("country"),
        index.SearchField("lat"),
        index.SearchField("lon"),
        index.SearchField("localized_country_name"),
        index.SearchField("name"),
        index.SearchField("phone"),
        index.SearchField("zip_code"),
    ]

    # api fields
    api_fields = [
        APIField("meetup_id"),
        APIField("address_1"),
        APIField("address_2"),
        APIField("address_3"),
        APIField("city"),
        APIField("country"),
        APIField("lat"),
        APIField("lon"),
        APIField("localized_country_name"),
        APIField("name"),
        APIField("phone"),
        APIField("zip_code"),
    ]


class EventPage(Page):
    """
    Meetup Event
    """

    # models
    meetup_id = models.CharField(max_length=255, unique=True)
    attendance_count = models.IntegerField(blank=True, null=True)
    attendance_sample = models.IntegerField(blank=True, null=True)
    attendee_sample = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    date_in_series_pattern = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)
    duration = models.DurationField(blank=True, null=True)
    fee_accepts = models.CharField(max_length=255, blank=True, null=True)
    fee_amount = models.FloatField(blank=True, null=True)
    fee_currency = models.CharField(max_length=255, blank=True, null=True)
    fee_description = models.TextField(blank=True, null=True)
    fee_label = models.CharField(max_length=255, blank=True, null=True)
    how_to_find_us = models.TextField(blank=True, null=True)
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=100, blank=True, null=True)
    time = models.DateTimeField()
    updated = models.DateTimeField(blank=True, null=True)
    utc_offset = models.IntegerField(blank=True, null=True)
    venue = models.ForeignKey(
        Venue, on_delete=models.SET_NULL, blank=True, null=True, related_name="+"
    )
    venue_visibility = models.CharField(max_length=255, blank=True, null=True)
    visibility = models.CharField(max_length=255, blank=True, null=True)

    # admin interface panels
    content_panels = Page.content_panels + [
        FieldPanel("meetup_id"),
        FieldPanel("attendance_count"),
        FieldPanel("attendance_sample"),
        FieldPanel("attendee_sample"),
        FieldPanel("created"),
        FieldPanel("date_in_series_pattern"),
        FieldPanel("description"),
        FieldPanel("duration"),
        InlinePanel("event_hosts", label="Event Hosts"),
        FieldPanel("fee_accepts"),
        FieldPanel("fee_amount"),
        FieldPanel("fee_currency"),
        FieldPanel("fee_description"),
        FieldPanel("fee_label"),
        FieldPanel("how_to_find_us"),
        FieldPanel("name"),
        FieldPanel("status"),
        FieldPanel("time"),
        FieldPanel("updated"),
        FieldPanel("utc_offset"),
        FieldPanel("venue"),
        FieldPanel("venue_visibility"),
        FieldPanel("visibility"),
    ]

    # Search index configuration
    search_fields = Page.search_fields + [
        index.SearchField("meetup_id"),
        index.SearchField("attendance_count"),
        index.SearchField("attendance_sample"),
        index.SearchField("created"),
        index.FilterField("date_in_series_pattern"),
        index.FilterField("description"),
        index.FilterField("fee_accepts"),
        index.FilterField("fee_amount"),
        index.FilterField("fee_currency"),
        index.FilterField("fee_description"),
        index.FilterField("fee_label"),
        index.FilterField("how_to_find_us"),
        index.FilterField("name"),
        index.FilterField("status"),
        index.FilterField("time"),
        index.FilterField("updated"),
        index.FilterField("venue"),
        index.FilterField("venue_visibility"),
        index.FilterField("visibility"),
    ]

    # api fields
    api_fields = [
        APIField("meetup_id"),
        APIField("attendance_count"),
        APIField("attendance_sample"),
        APIField("created"),
        APIField("date_in_series_pattern"),
        APIField("description"),
        APIField("duration"),
        APIField("event_hosts"),
        APIField("fee_accepts"),
        APIField("fee_amount"),
        APIField("fee_currency"),
        APIField("fee_description"),
        APIField("fee_label"),
        APIField("how_to_find_us"),
        APIField("name"),
        APIField("status"),
        APIField("time"),
        APIField("updated"),
        APIField("utc_offset"),
        APIField("venue"),
        APIField("venue_visibility"),
        APIField("visibility"),
    ]

    parent_page_types = ["meetup_scraper.GroupPage"]  # allow parent page types
    subpage_types = []  # no child pages allow


@register_snippet
class EventHost(models.Model):
    """
    Meetup Event Host
    """

    event_page = ParentalKey(
        EventPage, on_delete=models.CASCADE, related_name="event_hosts"
    )
    host_count = models.IntegerField(blank=True, null=True)
    member = models.ForeignKey(
        Member, on_delete=models.SET_NULL, blank=True, null=True, related_name="+"
    )
    intro = models.TextField(blank=True, null=True)
    join_date = models.DateTimeField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    photo = models.ForeignKey(
        Photo, on_delete=models.SET_NULL, blank=True, null=True, related_name="+"
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("member"),
        FieldPanel("host_count"),
        FieldPanel("intro"),
        FieldPanel("join_date"),
        FieldPanel("photo"),
    ]

    # Search index configuration
    search_fields = Page.search_fields + [
        index.SearchField("host_count"),
        index.SearchField("member"),
        index.SearchField("intro"),
        index.SearchField("join_date"),
        index.SearchField("name"),
        index.SearchField("photo"),
    ]

    # api fields
    api_fields = [
        APIField("host_count"),
        APIField("member_id"),
        APIField("intro"),
        APIField("time"),
        APIField("name"),
        APIField("photo"),
    ]


@register_snippet
class Category(models.Model):
    """
    Meetup Category
    """

    meetup_id = models.BigIntegerField(unique=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    shortname = models.CharField(max_length=255, blank=True, null=True)
    sort_name = models.CharField(max_length=255, blank=True, null=True)

    # admin interface panels
    panels = [
        FieldPanel("meetup_id"),
        FieldPanel("name"),
        FieldPanel("shortname"),
        FieldPanel("sort_name"),
    ]

    # Search index configuration
    search_fields = Page.search_fields + [
        index.SearchField("meetup_id"),
        index.SearchField("name"),
        index.SearchField("shortname"),
        index.SearchField("sort_name"),
    ]

    # api fields
    api_fields = [
        APIField("meetup_id"),
        APIField("name"),
        APIField("shortname"),
        APIField("sort_name"),
    ]


@register_snippet
class MetaCategory(models.Model):
    """
    Meetup Meta Category
    """

    meetup_id = models.BigIntegerField(unique=True)
    categories = models.ManyToManyField(Category, related_name="+")
    name = models.CharField(max_length=255)
    photo = models.ForeignKey(Photo, on_delete=models.SET_NULL, blank=True, null=True)
    shortname = models.CharField(max_length=255)
    sort_name = models.CharField(max_length=255)

    # admin interface panels
    panels = [
        FieldPanel("meetup_id"),
        FieldPanel("categories"),
        FieldPanel("name"),
        FieldPanel("photo"),
        FieldPanel("shortname"),
        FieldPanel("sort_name"),
    ]

    # Search index configuration
    search_fields = Page.search_fields + [
        index.SearchField("meetup_id"),
        index.SearchField("categories"),
        index.SearchField("name"),
        index.SearchField("photo"),
        index.SearchField("shortname"),
        index.SearchField("sort_name"),
    ]

    # api fields
    api_fields = [
        APIField("meetup_id"),
        APIField("categories"),
        APIField("name"),
        APIField("photo"),
        APIField("shortname"),
        APIField("sort_name"),
    ]


@register_snippet
class Topic(models.Model):
    """
    Meetup Topic
    """

    meetup_id = models.BigIntegerField(unique=True)
    lang = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    urlkey = models.CharField(max_length=255, unique=True)

    # admin interface panels
    panels = [
        FieldPanel("meetup_id"),
        FieldPanel("lang"),
        FieldPanel("name"),
        FieldPanel("urlkey"),
    ]

    # Search index configuration
    search_fields = Page.search_fields + [
        index.SearchField("meetup_id"),
        index.SearchField("lang"),
        index.SearchField("name"),
        index.SearchField("urlkey"),
    ]

    # api fields
    api_fields = [
        APIField("meetup_id"),
        APIField("lang"),
        APIField("name"),
        APIField("urlkey"),
    ]


class GroupPage(Page):
    """
    Meetup Group
    """

    # models
    meetup_id = models.BigIntegerField(unique=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, blank=True, null=True
    )
    city = models.CharField(max_length=255, blank=True, null=True)
    city_link = models.URLField(blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateTimeField()
    description = models.TextField()
    fee_options_currencies_code = models.CharField(
        max_length=255, blank=True, null=True
    )
    fee_options_currencies_default = models.BooleanField(blank=True, null=True)
    fee_options_type = models.CharField(max_length=255, blank=True, null=True)
    group_photo = models.ForeignKey(
        Photo,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="group_photo",
    )
    join_mode = models.CharField(max_length=255, blank=True, null=True)
    key_photo = models.ForeignKey(
        Photo,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="key_photo",
    )
    lat = models.DecimalField(max_digits=10, decimal_places=8)
    lon = models.DecimalField(max_digits=10, decimal_places=8)
    link = models.URLField()
    localized_country_name = models.CharField(max_length=255, blank=True, null=True)
    localized_location = models.CharField(max_length=255, blank=True, null=True)
    member_limit = models.IntegerField(blank=True, null=True)
    members = models.IntegerField()
    meta_category = models.ForeignKey(
        MetaCategory, on_delete=models.SET_NULL, blank=True, null=True, related_name="+"
    )
    name = models.CharField(max_length=100)
    nomination_acceptable = models.BooleanField(default=False)
    organizer = models.ForeignKey(
        Member, on_delete=models.SET_NULL, blank=True, null=True, related_name="+"
    )
    short_link = models.URLField(blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=100)
    timezone = models.CharField(max_length=255)
    topics = models.ManyToManyField(Topic, related_name="+")
    untranslated_city = models.CharField(max_length=255, blank=True, null=True)
    urlname = models.CharField(max_length=255, unique=True)
    visibility = models.CharField(max_length=255)
    welcome_message = models.TextField(blank=True, null=True)
    who = models.CharField(max_length=255, blank=True, null=True)

    # admin interface panels
    content_panels = Page.content_panels + [
        FieldPanel("meetup_id"),
        FieldPanel("category"),
        FieldPanel("city"),
        FieldPanel("city_link"),
        FieldPanel("country"),
        FieldPanel("created"),
        FieldPanel("description"),
        FieldPanel("fee_options_currencies_code"),
        FieldPanel("fee_options_currencies_default"),
        FieldPanel("fee_options_type"),
        FieldPanel("group_photo"),
        FieldPanel("join_mode"),
        FieldPanel("key_photo"),
        FieldPanel("lat"),
        FieldPanel("lon"),
        FieldPanel("link"),
        FieldPanel("localized_country_name"),
        FieldPanel("localized_location"),
        FieldPanel("member_limit"),
        FieldPanel("members"),
        FieldPanel("meta_category"),
        FieldPanel("name"),
        FieldPanel("nomination_acceptable"),
        FieldPanel("organizer"),
        FieldPanel("short_link"),
        FieldPanel("state"),
        FieldPanel("status"),
        FieldPanel("timezone"),
        FieldPanel("topics"),
        FieldPanel("untranslated_city"),
        FieldPanel("urlname"),
        FieldPanel("visibility"),
        FieldPanel("welcome_message"),
        FieldPanel("who"),
    ]

    # Search index configuration
    search_fields = Page.search_fields + [
        index.SearchField("meetup_id"),
        index.SearchField("category"),
        index.SearchField("city"),
        index.SearchField("city_link"),
        index.SearchField("country"),
        index.SearchField("created"),
        index.SearchField("description"),
        index.SearchField("fee_options_currencies_code"),
        index.SearchField("fee_options_currencies_default"),
        index.SearchField("fee_options_type"),
        index.SearchField("group_photo"),
        index.SearchField("join_mode"),
        index.SearchField("key_photo"),
        index.SearchField("lat"),
        index.SearchField("lon"),
        index.SearchField("link"),
        index.SearchField("localized_country_name"),
        index.SearchField("localized_location"),
        index.SearchField("member_limit"),
        index.SearchField("members"),
        index.SearchField("meta_category"),
        index.SearchField("name"),
        index.SearchField("nomination_acceptable"),
        index.SearchField("organizer"),
        index.SearchField("short_link"),
        index.SearchField("state"),
        index.SearchField("status"),
        index.SearchField("timezone"),
        index.SearchField("untranslated_city"),
        index.SearchField("urlname"),
        index.SearchField("visibility"),
        index.SearchField("welcome_message"),
        index.SearchField("who"),
    ]

    # api fields
    api_fields = [
        APIField("meetup_id"),
        APIField("category"),
        APIField("city"),
        APIField("city_link"),
        APIField("country"),
        APIField("created"),
        APIField("description"),
        APIField("fee_options_currencies_code"),
        APIField("fee_options_currencies_default"),
        APIField("fee_options_type"),
        APIField("group_photo"),
        APIField("join_mode"),
        APIField("key_photo"),
        APIField("lat"),
        APIField("lon"),
        APIField("link"),
        APIField("localized_country_name"),
        APIField("localized_location"),
        APIField("member_limit"),
        APIField("members"),
        APIField("meta_category"),
        APIField("name"),
        APIField("nomination_acceptable"),
        APIField("organizer"),
        APIField("short_link"),
        APIField("state"),
        APIField("status"),
        APIField("timezone"),
        APIField("topics"),
        APIField("untranslated_city"),
        APIField("urlname"),
        APIField("visibility"),
        APIField("welcome_message"),
        APIField("who"),
    ]

    parent_page_types = ["meetup_scraper.HomePage"]  # allow parent page types
    subpage_types = ["meetup_scraper.EventPage"]  # allow child page types

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
