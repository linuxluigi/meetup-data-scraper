import pytest
from .factories import (
    GroupPageFactory,
    EventPage1Factory,
    EventPage2Factory,
    EventPage3Factory,
    ImprintPageFactory,
    PrivacyPageFactory,
)
from meetup_data_scraper.meetup_scraper.models import (
    GroupPage,
    EventPage,
    SimplePage,
    HomePage,
    Venue,
)
from meetup_data_scraper.meetup_scraper.meetup_api_client.meetup_api_client import (
    MeetupApiClient,
)
import datetime
from meetup_data_scraper.meetup_scraper.tests.meetup_api_demo_response import (
    get_venue_response,
)
from meetup_data_scraper.meetup_scraper.meetup_api_client.json_parser import (
    get_venue_from_response,
)

pytestmark = pytest.mark.django_db


def test_venue_locastion():
    # set venue response
    venue_1_response: dict = get_venue_response(meetup_id=123, content=False)
    venue_2_response: dict = get_venue_response(meetup_id=124, content=True)

    # get venue model
    venue_1: Venue = get_venue_from_response(response=venue_1_response)
    venue_2: Venue = get_venue_from_response(response=venue_2_response)

    # assert venue with no lat & lon
    assert venue_1.location["lat"] == None
    assert venue_1.location["lon"] == None

    # assert venue with lat & lon
    assert "{0:.8f}".format(venue_2.location["lat"]) == "{0:.8f}".format(
        venue_2_response["lat"]
    )
    assert "{0:.8f}".format(venue_2.location["lon"]) == "{0:.8f}".format(
        venue_2_response["lon"]
    )


def test_meetup_page_locastion():
    # test meetup location on GroupPage
    sandbox_group: GroupPage = GroupPageFactory()

    assert "{0:.8f}".format(sandbox_group.location["lat"]) == "{0:.8f}".format(
        sandbox_group.lat
    )
    assert "{0:.8f}".format(sandbox_group.location["lon"]) == "{0:.8f}".format(
        sandbox_group.lon
    )

    sandbox_group.lat = None
    sandbox_group.lon = None

    assert sandbox_group.location["lat"] == None
    assert sandbox_group.location["lon"] == None


def test_venue_groups():
    # set venue response
    venue_response: dict = get_venue_response(meetup_id=123, content=False)

    # get venue model
    venue: Venue = get_venue_from_response(response=venue_response)

    # assert with empty group / event
    venue_groups: dict = venue.groups
    assert isinstance(venue_groups, dict)
    assert venue_groups == {}

    # add venue to event
    sandbox_group: GroupPage = GroupPageFactory()
    sandbox_event_1: EventPage = EventPage1Factory()
    sandbox_event_1.venue = venue
    sandbox_event_1.save()

    # assert with 1 group / 1 event
    venue_groups: dict = venue.groups
    assert isinstance(venue_groups, dict)
    assert isinstance(venue_groups[sandbox_group.pk], dict)
    assert len(venue_groups[sandbox_group.pk]["events"]) == 1

    # add more events
    sandbox_event_2: EventPage = EventPage2Factory()
    sandbox_event_2.venue = venue
    sandbox_event_2.save()
    sandbox_event_3: EventPage = EventPage3Factory()
    sandbox_event_3.venue = venue
    sandbox_event_3.save()

    # assert with 1 group / 3 event
    venue_groups: dict = venue.groups
    assert isinstance(venue_groups, dict)
    assert isinstance(venue_groups[sandbox_group.pk], dict)
    assert len(venue_groups[sandbox_group.pk]["events"]) == 3


def test_group_page_last_event():
    # test when there is no event
    sandbox_group: GroupPage = GroupPageFactory()
    assert sandbox_group.last_event() is None

    # test when there is a new event
    sandbox_event_1: EventPage = EventPage1Factory()
    assert sandbox_group.last_event().meetup_id == sandbox_event_1.meetup_id

    sandbox_event_2: EventPage = EventPage2Factory()
    EventPage3Factory()
    assert sandbox_group.last_event().meetup_id == sandbox_event_2.meetup_id

    # delete all events
    for event in sandbox_group.events():
        event.delete()

    # get 20 events from the sandbox group
    api_client: MeetupApiClient = MeetupApiClient()
    event_page_entries = 20
    api_client.update_group_events(group=sandbox_group, max_entries=event_page_entries)

    event_page_counter: int = 1
    for _ in sandbox_group.events():
        last_event: EventPage = sandbox_group.last_event()
        last_event_time: datetime = last_event.time
        last_event.delete()

        assert last_event_time is not None
        if sandbox_group.last_event():
            event_page_counter = event_page_counter + 1
            assert last_event_time > sandbox_group.last_event().time
    assert event_page_counter == event_page_entries


def test_group_page_events():
    # test when there is no event
    sandbox_group: GroupPage = GroupPageFactory()
    assert len(sandbox_group.events()) == 0

    # add one event
    EventPage1Factory()
    assert len(sandbox_group.events()) == 1

    # add tow events
    EventPage2Factory()
    EventPage3Factory()
    assert len(sandbox_group.events()) == 3


@pytest.mark.django_db()
def test_home_page_child_pages():
    # get home page
    api_client: MeetupApiClient = MeetupApiClient()
    home_page: HomePage = api_client.get_home_page()

    # test when there no child page
    assert len(home_page.child_pages) == 0

    # test with 1 child page
    ImprintPageFactory()
    assert len(home_page.child_pages) == 1

    # test with 1 child page
    PrivacyPageFactory()
    assert len(home_page.child_pages) == 2
