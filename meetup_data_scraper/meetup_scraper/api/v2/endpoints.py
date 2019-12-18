from wagtail.api.v2.endpoints import BaseAPIEndpoint, PagesAPIEndpoint
from meetup_data_scraper.meetup_scraper.models import (
    Category,
    EventHost,
    EventPage,
    GroupPage,
    MeetupPage,
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
from wagtail.core.models import Page


class VenueAPIEndpoint(BaseAPIEndpoint):
    model = Venue

    listing_default_fields = BaseAPIEndpoint.listing_default_fields + [
        "meetup_id",
        "address_1",
        "address_2",
        "address_3",
        "city",
        "country",
        "location",
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


class MeetupAPIEndpoint(PagesAPIEndpoint):
    model = MeetupPage

    listing_default_fields = PagesAPIEndpoint.listing_default_fields + [
        "name",
        "description",
        "location",
        "link",
        "shortname",
        "time",
    ]

    def get_queryset(self):
        request = self.request

        # Allow pages to be filtered to a specific type
        try:
            models = page_models_from_string(
                request.GET.get("type", "meetup_scraper.MeetupPage")
            )
        except (LookupError, ValueError):
            raise BadRequestError("type doesn't exist")

        if not models:
            models = [MeetupPage]

        if len(models) == 1:
            queryset = models[0].objects.all()
        else:
            queryset = Page.objects.all()

            # Filter pages by specified models
            queryset = filter_page_type(queryset, models)

        # Get live pages that are not in a private section
        queryset = queryset.public().live()

        # Filter by site
        if request.site:
            queryset = queryset.descendant_of(request.site.root_page, inclusive=True)
        else:
            # No sites configured
            queryset = queryset.none()

        return queryset
