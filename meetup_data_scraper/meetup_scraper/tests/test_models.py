import pytest
from .factories import (
    GroupPageFactory,
    EventPage1Factory,
    EventPage2Factory,
    EventPage3Factory,
    ImprintPageFactory,
    PrivacyPageFactory
)
from meetup_data_scraper.meetup_scraper.models import GroupPage, EventPage, SimplePage, HomePage
from meetup_data_scraper.meetup_scraper.meetup_api_client.meetup_api_client import MeetupApiClient
import datetime

pytestmark = pytest.mark.django_db


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
