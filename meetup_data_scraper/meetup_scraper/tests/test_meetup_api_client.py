import pytest
from meetup_data_scraper.meetup_scraper.meetup_api_client import (
    RateLimit,
    MeetupApiClient,
)
from meetup_data_scraper.meetup_scraper.exceptions import (
    HttpNotFoundError,
    HttpNotAccessibleError,
)
from meetup_data_scraper.meetup_scraper.models import HomePage, GroupPage, EventPage
import time
import requests
import requests_mock
from .factories import GroupPageFactory, sandbox_meetup_group


def test_wait_for_next_request():
    # setup RateLimit
    rate_limit: RateLimit = RateLimit()
    timestamp: float = time.time()
    rate_limit.reset_time = timestamp + 2

    # wait
    rate_limit.wait_for_next_request()

    # assert
    assert time.time() >= rate_limit.reset_time


def test_update_rate_limit():
    # set start timestamp
    timestamp: float = time.time()

    # setup fake http request
    session = requests.Session()
    adapter = requests_mock.Adapter()
    session.mount("mock", adapter)

    adapter.register_uri("GET", "mock://test.com", text="data")
    response = session.get("mock://test.com")

    # set fake response
    default_header_value = 30
    response.headers["X-RateLimit-Limit"] = str(default_header_value)
    response.headers["X-RateLimit-Remaining"] = str(default_header_value)
    response.headers["X-RateLimit-Reset"] = str(default_header_value)

    rate_limit: RateLimit = RateLimit()
    rate_limit.update_rate_limit(response=response)

    # assert
    assert rate_limit.limit == default_header_value
    assert rate_limit.remaining == default_header_value
    assert rate_limit.reset == default_header_value
    assert rate_limit.reset_time >= timestamp + default_header_value
    assert rate_limit.reset_time <= time.time() + default_header_value


@pytest.mark.django_db()
def test_get_home_page():
    api_client: MeetupApiClient = MeetupApiClient()
    home_page: HomePage = api_client.get_home_page()

    assert isinstance(home_page, HomePage)
    assert home_page.title == "Home"


def test_get():
    api_client: MeetupApiClient = MeetupApiClient()

    # todo add more exepctions
    with pytest.raises(HttpNotFoundError):
        api_client.get("blume/blume/blume")

    json: dict = api_client.get(sandbox_meetup_group["urlname"])
    assert isinstance(json, dict)
    assert json["id"] == sandbox_meetup_group["meetup_id"]


@pytest.mark.django_db()
def test_get_group():
    api_client: MeetupApiClient = MeetupApiClient()
    group: GroupPage = api_client.get_group(sandbox_meetup_group["urlname"])

    assert isinstance(group, GroupPage)
    assert group.meetup_id == sandbox_meetup_group["meetup_id"]


@pytest.mark.django_db()
def test_update_all_group_events():
    api_client: MeetupApiClient = MeetupApiClient()
    sandbox_group = GroupPageFactory()
    events: [EventPage] = api_client.update_all_group_events(sandbox_group)

    assert isinstance(events[0], EventPage)
    assert len(events) > 1


@pytest.mark.django_db()
def test_update_group_events():
    api_client: MeetupApiClient = MeetupApiClient()
    sandbox_group: GroupPage = api_client.get_group(
        group_urlname=sandbox_meetup_group["urlname"]
    )
    event_1: [EventPage] = api_client.update_group_events(
        group=sandbox_group, max_entries=1, offset=0
    )
    event_2: [EventPage] = api_client.update_group_events(
        group=sandbox_group, max_entries=3, offset=1
    )
    event_3: [EventPage] = api_client.update_group_events(
        group=sandbox_group, max_entries=2, offset=0
    )

    assert isinstance(event_1[0], EventPage)
    assert len(event_1) == 1
    assert isinstance(event_2[0], EventPage)
    assert len(event_2) == 3
    assert event_1[0] != event_2[0]
    assert len(event_3) == 1
    assert event_1[0] != event_3[0]
