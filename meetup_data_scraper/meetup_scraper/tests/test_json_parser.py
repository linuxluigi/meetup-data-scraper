import pytest
from meetup_data_scraper.meetup_scraper.meetup_api_client.json_parser import (
    get_event_from_response,
    get_group_from_response,
    get_photo_from_response,
    get_member_from_response,
    get_event_host_from_response,
    get_category_from_response,
    get_topic_from_response,
    get_meta_category_from_response,
    get_venue_from_response,
)
from meetup_data_scraper.meetup_scraper.meetup_api_client.meetup_api_client import (
    MeetupApiClient,
)
from meetup_data_scraper.meetup_scraper.models import (
    Category,
    EventPage,
    GroupPage,
    Member,
    MetaCategory,
    Photo,
    Topic,
    Venue,
    EventHost,
)
from .meetup_api_demo_response import get_group_response, get_photo_response
from django.utils import timezone
import pytz
from datetime import datetime, timedelta
from meetup_data_scraper.meetup_scraper.tests.meetup_api_demo_response import (
    get_category_response,
    get_event_host_response,
    get_event_response,
    get_member_response,
    get_meta_category_response,
    get_topic_response,
    get_venue_response,
)
from meetup_data_scraper.meetup_scraper.tests.factories import GroupPageFactory


@pytest.mark.django_db()
def test_get_event_from_response():
    timezone.activate(pytz.timezone("UTC"))

    group: GroupPage = GroupPageFactory()

    # set event page response
    event_1_response: dict = get_event_response(meetup_id="1", content=False)
    event_2_response: dict = get_event_response(meetup_id="2", content=True)

    # get photo model
    event_1: EventPage = get_event_from_response(response=event_1_response, group=group)
    event_2: EventPage = get_event_from_response(response=event_2_response, group=group)

    # assert event_1
    assert isinstance(event_1, EventPage)
    assert event_1.title == "{}: {}".format(
        event_1_response["id"], event_1_response["name"]
    )
    assert event_1.slug == event_1_response["id"]
    assert event_1.meetup_id == event_1_response["id"]
    assert event_1.name == event_1_response["name"]
    assert event_1.time == timezone.make_aware(
        datetime.fromtimestamp(event_1_response["time"] / 1000)
    )
    assert event_1.attendance_count is None
    assert event_1.attendance_sample is None
    assert event_1.attendee_sample is None
    assert event_1.created is None
    assert event_1.date_in_series_pattern is False
    assert event_1.description is None
    assert event_1.duration is None
    assert len(event_1.event_hosts.all()) == 0
    assert event_1.fee_accepts is None
    assert event_1.fee_amount is None
    assert event_1.fee_currency is None
    assert event_1.fee_description is None
    assert event_1.fee_label is None
    assert event_1.how_to_find_us is None
    assert event_1.status is None
    assert event_1.updated is None
    assert event_1.utc_offset is None
    assert event_1.venue is None
    assert event_1.venue_visibility is None
    assert event_1.visibility is None

    # assert event_2
    assert isinstance(event_2, EventPage)
    assert event_2.title == "{}: {}".format(
        event_2_response["id"], event_2_response["name"]
    )
    assert event_2.slug == event_2_response["id"]
    assert event_2.meetup_id == event_2_response["id"]
    assert event_2.name == event_2_response["name"]
    assert event_2.time == timezone.make_aware(
        datetime.fromtimestamp(event_2_response["time"] / 1000)
    )
    assert event_2.attendance_count == event_2_response["attendance_count"]
    assert event_2.attendance_sample == event_2_response["attendance_sample"]
    assert event_2.attendee_sample == event_2_response["attendee_sample"]
    assert event_2.created == timezone.make_aware(
        datetime.fromtimestamp(event_2_response["created"] / 1000)
    )
    assert event_2.date_in_series_pattern == event_2_response["date_in_series_pattern"]
    assert event_2.description == event_2_response["description"]
    assert event_2.duration == timedelta(seconds=event_2_response["duration"] / 1000)
    assert len(event_2.event_hosts.all()) == 1
    assert isinstance(event_2.event_hosts.all()[0], EventHost)
    assert event_2.fee_accepts == event_2_response["fee"]["accepts"]
    assert event_2.fee_amount == event_2_response["fee"]["amount"]
    assert event_2.fee_currency == event_2_response["fee"]["currency"]
    assert event_2.fee_description == event_2_response["fee"]["description"]
    assert event_2.fee_label == event_2_response["fee"]["label"]
    assert event_2.how_to_find_us == event_2_response["how_to_find_us"]
    assert event_2.status == event_2_response["status"]
    assert event_2.updated == timezone.make_aware(
        datetime.fromtimestamp(event_2_response["updated"] / 1000)
    )
    assert event_2.utc_offset == event_2_response["utc_offset"] / 1000
    assert isinstance(event_2.venue, Venue)
    assert event_2.venue_visibility == event_2_response["venue_visibility"]
    assert event_2.visibility == event_2_response["visibility"]

    # send broken responses
    event_without_name = get_event_response(meetup_id="3")
    del event_without_name["name"]
    assert get_event_from_response(response=event_without_name, group=group) is None

    event_without_time = get_event_response(meetup_id="4")
    del event_without_time["time"]
    assert get_event_from_response(response=event_without_time, group=group) is None

    event_without_id = get_event_response()
    del event_without_id["id"]
    assert get_event_from_response(response=event_without_id, group=group) is None


@pytest.mark.django_db()
def test_get_group_from_response():
    api_client: MeetupApiClient = MeetupApiClient()
    timezone.activate(pytz.timezone("UTC"))

    # set group page response
    group_1_response: dict = get_group_response(
        meetup_id=54654, urlname="group_1", content=False
    )
    group_2_response: dict = get_group_response(
        meetup_id=54655, urlname="group_2", content=True
    )
    group_3_response: dict = get_group_response(
        meetup_id=54656, urlname="group_3", content=True
    )
    del group_3_response["fee_options"]["currencies"]["default"]
    del group_3_response["nomination_acceptable"]

    # get photo model
    group_1: GroupPage = get_group_from_response(
        response=group_1_response, home_page=api_client.get_home_page()
    )
    group_2: GroupPage = get_group_from_response(
        response=group_2_response, home_page=api_client.get_home_page()
    )
    group_3: GroupPage = get_group_from_response(
        response=group_3_response, home_page=api_client.get_home_page()
    )

    # assert group_1
    assert isinstance(group_1, GroupPage)
    assert group_1.title == group_1_response["name"]
    assert group_1.slug == str(group_1_response["id"])
    assert group_1.meetup_id == group_1_response["id"]
    assert group_1.urlname == group_1_response["urlname"]
    assert group_1.created == timezone.make_aware(
        datetime.fromtimestamp(group_1_response["created"] / 1000)
    )
    assert group_1.description == group_1_response["description"]
    assert float(group_1.lat) == pytest.approx(group_1_response["lat"], 0.1)
    assert float(group_1.lon) == pytest.approx(group_1_response["lon"], 0.1)
    assert group_1.link == group_1_response["link"]
    assert group_1.members == group_1_response["members"]
    assert group_1.name == group_1_response["name"]
    assert group_2.nomination_acceptable is True
    assert group_1.status == group_1_response["status"]
    assert group_1.timezone == group_1_response["timezone"]
    assert group_1.visibility == group_1_response["visibility"]
    assert group_1.short_link is None
    assert group_1.welcome_message is None
    assert group_1.city is None
    assert group_1.city_link is None
    assert group_1.untranslated_city is None
    assert group_1.country is None
    assert group_1.localized_country_name is None
    assert group_1.localized_location is None
    assert group_1.state is None
    assert group_1.join_mode is None
    assert group_1.fee_options_currencies_code is None
    assert group_1.fee_options_currencies_default is None
    assert group_1.fee_options_type is None
    assert group_1.member_limit is None
    assert group_1.organizer is None
    assert group_1.who is None
    assert group_1.group_photo is None
    assert group_1.key_photo is None
    assert group_1.category is None
    assert len(group_1.topics.all()) == 0
    assert group_1.meta_category is None

    # assert group_2
    assert isinstance(group_2, GroupPage)
    assert group_2.title == group_2_response["name"]
    assert group_2.slug == str(group_2_response["id"])
    assert group_2.meetup_id == group_2_response["id"]
    assert group_2.urlname == group_2_response["urlname"]
    assert group_2.created == timezone.make_aware(
        datetime.fromtimestamp(group_2_response["created"] / 1000)
    )
    assert group_2.description == group_2_response["description"]
    assert float(group_2.lat) == pytest.approx(group_2_response["lat"], 0.1)
    assert float(group_2.lon) == pytest.approx(group_2_response["lon"], 0.1)
    assert group_2.link == group_2_response["link"]
    assert group_2.members == group_2_response["members"]
    assert group_2.name == group_2_response["name"]
    assert group_2.nomination_acceptable == group_2_response["nomination_acceptable"]
    assert group_2.status == group_2_response["status"]
    assert group_2.timezone == group_2_response["timezone"]
    assert group_2.visibility == group_2_response["visibility"]
    assert group_2.short_link == group_2_response["short_link"]
    assert group_2.welcome_message == group_2_response["welcome_message"]
    assert group_2.city == group_2_response["city"]
    assert group_2.city_link == group_2_response["city_link"]
    assert group_2.untranslated_city == group_2_response["untranslated_city"]
    assert group_2.country == group_2_response["country"]
    assert group_2.localized_country_name == group_2_response["localized_country_name"]
    assert group_2.localized_location == group_2_response["localized_location"]
    assert group_2.state == group_2_response["state"]
    assert group_2.join_mode == group_2_response["join_mode"]
    assert (
        group_2.fee_options_currencies_code
        == group_2_response["fee_options"]["currencies"]["code"]
    )
    assert (
        group_2.fee_options_currencies_default
        == group_2_response["fee_options"]["currencies"]["default"]
    )
    assert group_2.fee_options_type == group_2_response["fee_options"]["type"]
    assert group_2.member_limit == group_2_response["member_limit"]
    assert isinstance(group_2.organizer, Member)
    assert group_2.who == group_2_response["who"]
    assert isinstance(group_2.group_photo, Photo)
    assert isinstance(group_2.key_photo, Photo)
    assert isinstance(group_2.category, Category)
    assert len(group_2.topics.all()) == 1
    assert isinstance(group_2.topics.all()[0], Topic)
    assert isinstance(group_2.meta_category, MetaCategory)

    # assert group_3
    assert (
        group_3.fee_options_currencies_code
        == group_3_response["fee_options"]["currencies"]["code"]
    )
    assert group_3.fee_options_currencies_default is False
    assert group_3.fee_options_type == group_3_response["fee_options"]["type"]
    assert group_3.nomination_acceptable is False


@pytest.mark.django_db()
def test_get_photo_from_response():
    # set photo response
    photo_1_response: dict = get_photo_response(
        meetup_id=1, photo_type="event", content=True
    )
    photo_2_response: dict = get_photo_response(
        meetup_id=2, photo_type="member", content=True
    )
    photo_3_response: dict = get_photo_response(meetup_id=3)

    # get photo model
    photo_1: Photo = get_photo_from_response(response=photo_1_response)
    photo_2: Photo = get_photo_from_response(response=photo_2_response)
    photo_3: Photo = get_photo_from_response(response=photo_3_response)

    # assert photo_1
    assert isinstance(photo_1, Photo)
    assert photo_1.meetup_id == photo_1_response["id"]
    assert photo_1.photo_type == photo_1_response["type"]
    assert photo_1.highres_link == photo_1_response["highres_link"]
    assert photo_1.photo_link == photo_1_response["photo_link"]
    assert photo_1.thumb_link == photo_1_response["thumb_link"]
    assert photo_1.base_url == photo_1_response["base_url"]

    # assert photo_2
    assert isinstance(photo_2, Photo)
    assert photo_2.meetup_id == photo_2_response["id"]
    assert photo_2.photo_type == photo_2_response["type"]
    assert photo_2.highres_link == photo_2_response["highres_link"]
    assert photo_2.photo_link == photo_2_response["photo_link"]
    assert photo_2.thumb_link == photo_2_response["thumb_link"]
    assert photo_2.base_url == photo_2_response["base_url"]

    # assert photo_3
    assert isinstance(photo_3, Photo)
    assert photo_3.meetup_id == photo_3_response["id"]
    assert photo_3.photo_type is None
    assert photo_3.highres_link is None
    assert photo_3.photo_link is None
    assert photo_3.thumb_link is None
    assert photo_3.base_url is None


@pytest.mark.django_db()
def test_get_member_from_response():
    # set member response
    member_1_response: dict = get_member_response(meetup_id=1, content=False)
    member_2_response: dict = get_member_response(meetup_id=2, content=True)

    # get member model
    member_1: Member = get_member_from_response(response=member_1_response)
    member_2: Member = get_member_from_response(response=member_2_response)

    # assert member_1
    assert isinstance(member_1, Member)
    assert member_1.meetup_id == member_1_response["id"]
    assert member_1.name is None
    assert member_1.bio is None
    assert member_1.photo is None

    # assert member_2
    assert isinstance(member_2, Member)
    assert member_2.meetup_id == member_2_response["id"]
    assert member_2.name == member_2_response["name"]
    assert member_2.bio == member_2_response["bio"]
    assert isinstance(member_2.photo, Photo)


@pytest.mark.django_db()
def test_get_event_host_from_response():
    timezone.activate(pytz.timezone("UTC"))

    # set event host response
    event_host_1_response: dict = get_event_host_response(content=False)
    event_host_2_response: dict = get_event_host_response(content=True)

    # get event host model
    event_host_1: EventHost = get_event_host_from_response(
        response=event_host_1_response
    )
    event_host_2: EventHost = get_event_host_from_response(
        response=event_host_2_response
    )

    # assert event_host_1
    assert isinstance(event_host_1, EventHost)
    assert event_host_1.host_count is None
    assert event_host_1.member is None
    assert event_host_1.intro is None
    assert event_host_1.join_date is None
    assert event_host_1.name is None
    assert event_host_1.photo is None

    # assert event_host_2
    assert isinstance(event_host_2, EventHost)
    assert event_host_2.host_count == event_host_2_response["host_count"]
    assert isinstance(event_host_2.member, Member)
    assert event_host_2.intro == event_host_2_response["intro"]
    assert event_host_2.join_date == timezone.make_aware(
        datetime.fromtimestamp(event_host_2_response["join_date"] / 1000)
    )
    assert event_host_2.name == event_host_2_response["name"]
    assert isinstance(event_host_2.photo, Photo)


@pytest.mark.django_db()
def test_get_category_from_response():
    # set category response
    category_1_response: dict = get_category_response(content=False)
    category_2_response: dict = get_category_response(content=True)

    # get categoryt model
    category_1: Category = get_category_from_response(response=category_1_response)
    category_2: Category = get_category_from_response(response=category_2_response)

    # assert category_1
    assert isinstance(category_1, Category)
    assert category_1.meetup_id == category_1_response["id"]
    assert category_1.name is None
    assert category_1.shortname is None
    assert category_1.sort_name is None

    # assert category_2
    assert isinstance(category_2, Category)
    assert category_2.meetup_id == category_2_response["id"]
    assert category_2.name == category_2_response["name"]
    assert category_2.shortname == category_2_response["shortname"]
    assert category_2.sort_name == category_2_response["sort_name"]


@pytest.mark.django_db()
def test_get_topic_from_response():
    # set topic response
    topic_response: dict = get_topic_response()

    # get categoryt model
    topic: Topic = get_topic_from_response(response=topic_response)

    # assert topic
    assert isinstance(topic, Topic)
    assert topic.meetup_id == topic_response["id"]
    assert topic.lang == topic_response["lang"]
    assert topic.name == topic_response["name"]
    assert topic.urlkey == topic_response["urlkey"]


@pytest.mark.django_db()
def test_get_meta_category_from_response():
    # set meta category response
    meta_category_1_response: dict = get_meta_category_response(
        meetup_id=123, content=False
    )
    meta_category_2_response: dict = get_meta_category_response(
        meetup_id=124, content=True
    )

    # get categoryt model
    meta_category_1: MetaCategory = get_meta_category_from_response(
        response=meta_category_1_response
    )
    meta_category_2: MetaCategory = get_meta_category_from_response(
        response=meta_category_2_response
    )

    # assert meta_category_1
    assert isinstance(meta_category_1, MetaCategory)
    assert meta_category_1.meetup_id == meta_category_1_response["id"]
    assert len(meta_category_1.categories.all()) == 0
    assert meta_category_1.name == meta_category_1_response["name"]
    assert meta_category_1.photo is None
    assert meta_category_1.shortname == meta_category_1_response["shortname"]
    assert meta_category_1.sort_name == meta_category_1_response["sort_name"]

    # assert meta_category_2
    assert isinstance(meta_category_2, MetaCategory)
    assert meta_category_2.meetup_id == meta_category_2_response["id"]
    assert isinstance(meta_category_2.categories.all()[0], Category)
    assert meta_category_2.name == meta_category_2_response["name"]
    assert isinstance(meta_category_2.photo, Photo)
    assert meta_category_2.shortname == meta_category_2_response["shortname"]
    assert meta_category_2.sort_name == meta_category_2_response["sort_name"]


@pytest.mark.django_db()
def test_get_venue_from_response():
    # set venue response
    venue_1_response: dict = get_venue_response(meetup_id=123, content=False)
    venue_2_response: dict = get_venue_response(meetup_id=124, content=True)

    # get venue model
    venue_1: Venue = get_venue_from_response(response=venue_1_response)
    venue_2: Venue = get_venue_from_response(response=venue_2_response)

    # assert venue_1
    assert isinstance(venue_1, Venue)
    assert venue_1.meetup_id == venue_1_response["id"]
    assert venue_1.address_1 is None
    assert venue_1.address_2 is None
    assert venue_1.address_3 is None
    assert venue_1.city is None
    assert venue_1.country is None
    assert venue_1.lat is None
    assert venue_1.lon is None
    assert venue_1.localized_country_name is None
    assert venue_1.name is None
    assert venue_1.phone is None
    assert venue_1.zip_code is None

    # assert venue_2
    assert isinstance(venue_2, Venue)
    assert venue_2.meetup_id == venue_2_response["id"]
    assert venue_2.address_1 == venue_2_response["address_1"]
    assert venue_2.address_2 == venue_2_response["address_2"]
    assert venue_2.address_3 == venue_2_response["address_3"]
    assert venue_2.city == venue_2_response["city"]
    assert venue_2.country == venue_2_response["country"]
    assert venue_2.lat == venue_2_response["lat"]
    assert venue_2.lon == venue_2_response["lon"]
    assert venue_2.localized_country_name == venue_2_response["localized_country_name"]
    assert venue_2.name == venue_2_response["name"]
    assert venue_2.phone == venue_2_response["phone"]
    assert venue_2.zip_code == venue_2_response["zip_code"]
