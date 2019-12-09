import pytest
from meetup_data_scraper.meetup_scraper.meetup_api_client.meetup_api_client import (
    RateLimit,
    MeetupApiClient,
)
from meetup_data_scraper.meetup_scraper.meetup_api_client.exceptions import (
    HttpNoSuccess,
    HttpNotFoundError,
    HttpNotAccessibleError,
    HttpNoXRateLimitHeader,
)
from meetup_data_scraper.meetup_scraper.models import HomePage, GroupPage, EventPage
import time
import requests
import requests_mock
from .factories import GroupPageFactory, NotExistGroupPageFactory, meetup_groups
from pytest_httpserver import HTTPServer


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

    # use fake response without RateLimit headers
    rate_limit: RateLimit = RateLimit()
    with pytest.raises(HttpNoXRateLimitHeader):
        rate_limit.update_rate_limit(response=response, reset_time=2)

    # set fake response
    default_header_value = 30
    response.headers["X-RateLimit-Limit"] = str(default_header_value)
    response.headers["X-RateLimit-Remaining"] = str(default_header_value)
    response.headers["X-RateLimit-Reset"] = str(default_header_value)

    rate_limit: RateLimit = RateLimit()
    rate_limit.update_rate_limit(response=response, reset_time=2)

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


def test_get(httpserver: HTTPServer):
    api_client: MeetupApiClient = MeetupApiClient()

    with pytest.raises(HttpNotFoundError):
        api_client.get(meetup_groups["not-exist"]["urlname"])

    with pytest.raises(HttpNotAccessibleError):
        api_client.get(meetup_groups["gone"]["urlname"])

    json: dict = api_client.get(meetup_groups["sandbox"]["urlname"])
    assert isinstance(json, dict)
    assert json["id"] == meetup_groups["sandbox"]["meetup_id"]

    # test for HttpNoXRateLimitHeader execption
    for _ in range(4):
        httpserver.expect_oneshot_request("/HttpNoXRateLimitHeader").respond_with_data(
            "OK"
        )
    api_client.base_url = httpserver.url_for("/HttpNoXRateLimitHeader")
    with pytest.raises(HttpNoXRateLimitHeader):
        api_client.get(url_path="", reset_time=2)

    # test for HttpNoSuccess execption
    for _ in range(4):
        httpserver.expect_oneshot_request("/HttpNoSuccess")
    api_client.base_url = httpserver.url_for("")
    with pytest.raises(HttpNoSuccess):
        api_client.get(url_path="/", reset_time=2)


@pytest.mark.django_db()
def test_get_group(httpserver: HTTPServer):
    api_client: MeetupApiClient = MeetupApiClient()
    sandbox_group: GroupPage = api_client.get_group(meetup_groups["sandbox"]["urlname"])

    assert isinstance(sandbox_group, GroupPage)
    assert sandbox_group.meetup_id == meetup_groups["sandbox"]["meetup_id"]

    # test with gone group
    none_group: GroupPage = api_client.get_group(meetup_groups["gone"]["urlname"])
    assert none_group is None

    # test without existing group in database
    none_group: GroupPage = api_client.get_group(meetup_groups["not-exist"]["urlname"])
    assert none_group is None

    # test with existing group in database
    NotExistGroupPageFactory()
    none_group: GroupPage = api_client.get_group(meetup_groups["not-exist"]["urlname"])
    assert none_group is None
    not_exist_groups = GroupPage.objects.filter(
        urlname=meetup_groups["not-exist"]["urlname"]
    )
    assert not_exist_groups.exists() is False

    sandbox_group: GroupPage = GroupPageFactory()

    # test for HttpNoXRateLimitHeader execption
    httpserver.expect_oneshot_request(
        "/{}".format(sandbox_group.urlname)
    ).respond_with_data("OK")
    api_client.base_url = httpserver.url_for("/")
    none_group = api_client.get_group(sandbox_group.urlname)
    assert none_group is None
    sandbox_group_datbase = GroupPage.objects.filter(urlname=sandbox_group.urlname)
    assert sandbox_group_datbase.exists() is True

    # test for HttpNoSuccess execption
    httpserver.expect_oneshot_request("/HttpNoSuccess").respond_with_data("OK")
    api_client.base_url = httpserver.url_for("/HttpNoSuccess")
    none_group = api_client.get_group(sandbox_group.urlname)
    assert none_group is None
    sandbox_group_datbase = GroupPage.objects.filter(urlname=sandbox_group.urlname)
    assert sandbox_group_datbase.exists() is True


@pytest.mark.django_db()
def test_update_all_group_events():
    # set api_client & sandbox group
    api_client: MeetupApiClient = MeetupApiClient()
    sandbox_group: GroupPage = GroupPageFactory()

    # delte all events from group
    for event in sandbox_group.events():
        event.delete()

    # update sandbox group
    events: [EventPage] = api_client.update_all_group_events(group=sandbox_group)
    assert isinstance(events[0], EventPage)
    assert len(events) > 1

    # update non exist group
    not_exist_group: GroupPage = NotExistGroupPageFactory()
    none_group_events: [EventPage] = api_client.update_all_group_events(
        group=not_exist_group
    )
    assert len(none_group_events) == 0

    # delte last event
    sandbox_group.last_event().delete()

    # update sandbox group with max_entries_per_page of 300
    events: [EventPage] = api_client.update_all_group_events(
        group=sandbox_group, max_entries_per_page=300
    )
    assert isinstance(events[0], EventPage)

    # delte last event
    sandbox_group.last_event().delete()

    # update sandbox group with max_entries_per_page of -10
    events: [EventPage] = api_client.update_all_group_events(
        group=sandbox_group, max_entries_per_page=-10
    )
    assert isinstance(events[0], EventPage)


@pytest.mark.django_db()
def test_update_group_events(httpserver: HTTPServer):
    api_client: MeetupApiClient = MeetupApiClient()
    sandbox_group: GroupPage = api_client.get_group(
        group_urlname=meetup_groups["sandbox"]["urlname"]
    )
    event_1: [EventPage] = api_client.update_group_events(
        group=sandbox_group, max_entries=1, offset=0
    )
    event_2: [EventPage] = api_client.update_group_events(
        group=sandbox_group, max_entries=3, offset=1
    )
    event_3: [EventPage] = api_client.update_group_events(
        group=sandbox_group, max_entries=2, offset=-10
    )

    assert isinstance(event_1[0], EventPage)
    assert len(event_1) == 1
    assert isinstance(event_2[0], EventPage)
    assert len(event_2) == 3
    assert event_1[0] != event_2[0]
    assert len(event_3) == 1
    assert event_1[0] != event_3[0]

    not_exist_group: GroupPage = NotExistGroupPageFactory()
    none_group_events: [EventPage] = api_client.update_group_events(
        group=not_exist_group
    )

    assert len(none_group_events) == 0

    # delete all events from sandbox group
    sandbox_group_events: [EventPage] = sandbox_group.events()
    for event in sandbox_group_events:
        event.delete()

    # test for HttpNoXRateLimitHeader execption
    httpserver.expect_oneshot_request(
        "{}/events?status=past&page=1&offset=0".format(sandbox_group.urlname)
    ).respond_with_data("OK")
    api_client.base_url = httpserver.url_for("/")
    event_4: [EventPage] = api_client.update_group_events(
        group=sandbox_group, max_entries=1, offset=0
    )
    assert len(event_4) == 0

    # test for HttpNoSuccess execption
    httpserver.expect_oneshot_request("/HttpNoSuccess").respond_with_data("OK")
    api_client.base_url = httpserver.url_for("/HttpNoSuccess")
    event_5: [EventPage] = api_client.update_group_events(
        group=sandbox_group, max_entries=1, offset=0
    )
    assert len(event_5) == 0
