from wagtail.api.v2.endpoints import BaseAPIEndpoint, PagesAPIEndpoint
from meetup_data_scraper.meetup_scraper.models import (
    Category,
    EventHost,
    EventPage,
    GroupPage,
    Member,
    MetaCategory,
    Photo,
    Venue,
)
from wagtail.api.v2.utils import (
    BadRequestError,
    filter_page_type,
    page_models_from_string,
)


class VenueAPIEndpoint(BaseAPIEndpoint):
    model = Venue

    listing_default_fields = BaseAPIEndpoint.listing_default_fields + [
        "meetup_id",
        "address_1",
        "address_2",
        "address_3",
        "city",
        "country",
        "lat",
        "lon",
        "localized_country_name",
        "name",
        "phone",
        "zip_code",
    ]

    nested_default_fields = listing_default_fields


class PhotoAPIEndpoint(BaseAPIEndpoint):
    model = Photo

    listing_default_fields = BaseAPIEndpoint.listing_default_fields + [
        "meetup_id",
        "highres_link",
        "photo_link",
        "thumb_link",
        "photo_type",
        "base_url",
    ]

    nested_default_fields = listing_default_fields


class MemberAPIEndpoint(BaseAPIEndpoint):
    model = Member

    listing_default_fields = BaseAPIEndpoint.listing_default_fields + [
        "meetup_id",
        "name",
        "bio",
        "photo",
    ]

    nested_default_fields = listing_default_fields


class CategoryAPIEndpoint(BaseAPIEndpoint):
    model = Category

    listing_default_fields = BaseAPIEndpoint.listing_default_fields + [
        "meetup_id",
        "name",
        "shortname",
        "sort_name",
    ]

    nested_default_fields = listing_default_fields


class MetaCategoryAPIEndpoint(BaseAPIEndpoint):
    model = MetaCategory

    listing_default_fields = BaseAPIEndpoint.listing_default_fields + [
        "meetup_id",
        "categories",
        "name",
        "photo",
        "shortname",
        "sort_name",
    ]

    nested_default_fields = listing_default_fields


class EventHostAPIEndpoint(BaseAPIEndpoint):
    model = EventHost

    listing_default_fields = BaseAPIEndpoint.listing_default_fields + [
        "event_page",
        "host_count",
        "member",
        "intro",
        "join_date",
        "name",
        "photo",
    ]

    nested_default_fields = listing_default_fields


class EventPageAPIEndpoint(PagesAPIEndpoint):
    model = EventPage

    listing_default_fields = PagesAPIEndpoint.listing_default_fields + [
        "meetup_id",
        "attendance_count",
        "attendance_sample",
        "attendee_sample",
        "created",
        "date_in_series_pattern",
        "description",
        "duration",
        "event_hosts",
        "fee_accepts",
        "fee_amount",
        "fee_currency",
        "fee_description",
        "fee_label",
        "how_to_find_us",
        "name",
        "status",
        "time",
        "updated",
        "utc_offset",
        "venue",
        "venue_visibility",
        "visibility",
    ]

    nested_default_fields = listing_default_fields

    def get_queryset(self):
        request = self.request

        models = [EventPage]

        if len(models) == 1:
            queryset = models[0].objects.all()
        else:
            queryset = EventPage.objects.all()

            # Filter pages by specified models
            queryset = filter_page_type(queryset, models)

        # Get live pages that are not in a private section
        queryset = queryset.public().live()

        return queryset


class GroupPageAPIEndpoint(PagesAPIEndpoint):
    model = GroupPage

    listing_default_fields = PagesAPIEndpoint.listing_default_fields + [
        "meetup_id",
        "category",
        "city",
        "city_link",
        "country",
        "created",
        "description",
        "fee_options_currencies_code",
        "fee_options_currencies_default",
        "fee_options_type",
        "group_photo",
        "join_mode",
        "key_photo",
        "lat",
        "lon",
        "link",
        "localized_country_name",
        "localized_location",
        "member_limit",
        "members",
        "meta_category",
        "name",
        "nomination_acceptable",
        "organizer",
        "short_link",
        "state",
        "status",
        "timezone",
        "topics",
        "untranslated_city",
        "urlname",
        "visibility",
        "welcome_message",
        "who",
    ]

    nested_default_fields = listing_default_fields

    def get_queryset(self):
        request = self.request

        models = [GroupPage]

        if len(models) == 1:
            queryset = models[0].objects.all()
        else:
            queryset = EventPage.objects.all()

            # Filter pages by specified models
            queryset = filter_page_type(queryset, models)

        # Get live pages that are not in a private section
        queryset = queryset.public().live()

        return queryset
