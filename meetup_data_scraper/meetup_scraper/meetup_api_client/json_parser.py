from datetime import datetime, timedelta
from django.utils import timezone
from meetup_data_scraper.meetup_scraper.models import (
    Category,
    EventHost,
    EventPage,
    GroupPage,
    HomePage,
    Member,
    MetaCategory,
    Photo,
    Topic,
    Venue,
)


def get_event_from_response(response: dict, group: GroupPage) -> EventPage:
    """
    parse json response and return an EventPage

    Keyword arguments:
    response -- meetup api response in a dict

    return -> EventPage when not already exists
    """

    # if event page already exists, return None
    try:
        if EventPage.objects.filter(meetup_id=response["id"]).exists():
            return
    except KeyError:
        return

    try:
        # create event
        event: EventPage = EventPage(
            meetup_id=str(response["id"]),
            title="{}: {}".format(response["id"], response["name"]),
            name=response["name"],
            slug=response["id"],
            time=timezone.make_aware(datetime.fromtimestamp(response["time"] / 1000)),
        )
    except KeyError:
        return

    # add optional fields
    if "attendance_count" in response:
        event.attendance_count = response["attendance_count"]
    if "attendance_sample" in response:
        event.attendance_sample = response["attendance_sample"]
    if "attendee_sample" in response:
        event.attendee_sample = response["attendee_sample"]
    if "created" in response:
        event.created = timezone.make_aware(
            datetime.fromtimestamp(response["created"] / 1000)
        )
    if "date_in_series_pattern" in response:
        event.date_in_series_pattern = response["date_in_series_pattern"]
    if "description" in response:
        event.description = response["description"]
    if "duration" in response:
        event.duration = timedelta(seconds=response["duration"] / 1000)
    if "event_hosts" in response:
        event_hosts: [EventHost] = []
        for event_host in response["event_hosts"]:
            event_hosts.append(get_event_host_from_response(response=event_host))
        event.event_hosts = event_hosts
    else:
        event.event_hosts = []
    if "fee" in response:
        event.fee_accepts = response["fee"]["accepts"]
        event.fee_amount = response["fee"]["amount"]
        event.fee_currency = response["fee"]["currency"]
        event.fee_description = response["fee"]["description"]
        event.fee_label = response["fee"]["label"]
    if "how_to_find_us" in response:
        event.how_to_find_us = response["how_to_find_us"]
    if "status" in response:
        event.status = response["status"]
    if "utc_offset" in response:
        event.utc_offset = response["utc_offset"] / 1000
    if "updated" in response:
        event.updated = timezone.make_aware(
            datetime.fromtimestamp(response["updated"] / 1000)
        )
    if "venue" in response:
        event.venue = get_venue_from_response(response=response["venue"])
    if "venue_visibility" in response:
        event.venue_visibility = response["venue_visibility"]
    if "visibility" in response:
        event.visibility = response["visibility"]

    group.add_child(instance=event)
    event.save_revision().publish()
    return event


def get_group_from_response(response: dict, home_page: HomePage) -> GroupPage:
    """
    parse json response and return an EventPage

    Keyword arguments:
    response -- meetup api response in a dict
    home_page -- HomePage parent of GroupPage

    return -> get or create GroupPage based on urlname
    """

    # get or create the group page
    try:
        group: GroupPage = GroupPage.objects.get(urlname=response["urlname"])
    except GroupPage.DoesNotExist:
        group: GroupPage = GroupPage(
            title=response["name"],
            slug=response["id"],
            urlname=response["urlname"],
            meetup_id=response["id"],
            created=timezone.make_aware(
                datetime.fromtimestamp(response["created"] / 1000)
            ),
            description=response["description"],
            lat=response["lat"],
            lon=response["lon"],
            link=response["link"],
            members=response["members"],
            name=response["name"],
            status=response["status"],
            timezone=response["timezone"],
            visibility=response["visibility"],
        )

        # add group page as child of home page
        home_page.add_child(instance=group)

    # update required fields
    group.description = response["description"]
    group.link = response["link"]
    group.members = response["members"]
    group.name = response["name"]
    group.status = response["status"]
    group.timezone = response["timezone"]
    group.visibility = response["visibility"]

    # add optional fields
    if "category" in response:
        group.category = get_category_from_response(response=response["category"])
    if "city" in response:
        group.city = response["city"]
    if "city_link" in response:
        group.city_link = response["city_link"]
    if "country" in response:
        group.country = response["country"]
    if "fee_options" in response:
        if "currencies" in response["fee_options"]:
            group.fee_options_currencies_code = response["fee_options"]["currencies"][
                "code"
            ]
            if "default" in response["fee_options"]["currencies"]:
                group.fee_options_currencies_default = response["fee_options"][
                    "currencies"
                ]["default"]
            else:
                group.fee_options_currencies_default = False
        if "type" in response["fee_options"]:
            group.fee_options_type = response["fee_options"]["type"]
    if "group_photo" in response:
        group.group_photo = get_photo_from_response(response["group_photo"])
    if "join_mode" in response:
        group.join_mode = response["join_mode"]
    if "join_mode" in response:
        group.join_mode = response["join_mode"]
    if "key_photo" in response:
        group.key_photo = get_photo_from_response(response["key_photo"])
    if "lat" in response:
        group.lat = response["lat"]
    if "lon" in response:
        group.lon = response["lon"]
    if "localized_country_name" in response:
        group.localized_country_name = response["localized_country_name"]
    if "localized_location" in response:
        group.localized_location = response["localized_location"]
    if "member_limit" in response:
        group.member_limit = response["member_limit"]
    if "meta_category" in response:
        group.meta_category = get_meta_category_from_response(
            response=response["meta_category"]
        )
    else:
        group.nominated_member = False
    if "nomination_acceptable" in response:
        group.nomination_acceptable = True
    else:
        group.nomination_acceptable = False
    if "organizer" in response:
        group.organizer = get_member_from_response(response=response["organizer"])
    if "short_link" in response:
        group.short_link = response["short_link"]
    if "state" in response:
        group.state = response["state"]
    if "status" in response:
        group.status = response["status"]
    if "topics" in response:
        group.topics.clear()
        for topic in response["topics"]:
            group.topics.add(get_topic_from_response(response=topic))
    if "untranslated_city" in response:
        group.untranslated_city = response["untranslated_city"]
    if "welcome_message" in response:
        group.welcome_message = response["welcome_message"]
    if "who" in response:
        group.who = response["who"]

    # save & publish group
    group.save_revision().publish()

    return group


def get_photo_from_response(response: dict):
    """
    parse json response and return an Photo

    Keyword arguments:
    response -- meetup api response in a dict

    return -> get or create Photo
    """

    photo, create = Photo.objects.get_or_create(meetup_id=response["id"])

    # add optional fields
    if "highres_link" in response:
        photo.highres_link = response["highres_link"]
    if "base_url" in response:
        photo.base_url = response["base_url"]
    if "photo_link" in response:
        photo.photo_link = response["photo_link"]
    if "thumb_link" in response:
        photo.thumb_link = response["thumb_link"]
    if "type" in response:
        photo.photo_type = response["type"]

    photo.save()
    return photo


def get_member_from_response(response: dict):
    """
    parse json response and return an Member

    Keyword arguments:
    response -- meetup api response in a dict

    return -> get or create Member
    """

    member, create = Member.objects.get_or_create(meetup_id=response["id"])

    # add optional fields
    if "name" in response:
        member.name = response["name"]
    if "bio" in response:
        member.bio = response["bio"]
    if "photo" in response:
        member.photo = get_photo_from_response(response=response["photo"])

    member.save()
    return member


def get_event_host_from_response(response: dict):
    """
    parse json response and return an EventHost

    Keyword arguments:
    response -- meetup api response in a dict

    return -> get unsaved EventHost
    """

    event_host: EventHost = EventHost()

    # add optional fields
    if "host_count" in response:
        event_host.host_count = response["host_count"]
    if "id" in response:
        event_host.member = get_member_from_response(response={"id": response["id"]})
    if "intro" in response:
        event_host.intro = response["intro"]
    if "join_date" in response:
        event_host.join_date = timezone.make_aware(
            datetime.fromtimestamp(response["join_date"] / 1000)
        )
    if "name" in response:
        event_host.name = response["name"]
    if "photo" in response:
        event_host.photo = get_photo_from_response(response=response["photo"])

    return event_host


def get_category_from_response(response: dict):
    """
    parse json response and return an Category

    Keyword arguments:
    response -- meetup api response in a dict

    return -> get or create Category
    """

    category, create = Category.objects.get_or_create(meetup_id=response["id"])

    if "name" in response:
        category.name = response["name"]
    if "shortname" in response:
        category.shortname = response["shortname"]
    if "sort_name" in response:
        category.sort_name = response["sort_name"]

    category.save()
    return category


def get_topic_from_response(response: dict):
    """
    parse json response and return an Topic

    Keyword arguments:
    response -- meetup api response in a dict

    return -> get or create Topic
    """

    try:
        topic: Topic = Topic.objects.get(meetup_id=response["id"])
    except Topic.DoesNotExist:
        topic: Topic = Topic(
            meetup_id=response["id"],
            lang=response["lang"],
            name=response["name"],
            urlkey=response["urlkey"],
        )

    # update required fields
    topic.lang = response["lang"]
    topic.name = response["name"]
    topic.urlkey = response["urlkey"]

    topic.save()
    return topic


def get_meta_category_from_response(response: dict):
    """
    parse json response and return an MetaCategory

    Keyword arguments:
    response -- meetup api response in a dict

    return -> get or create MetaCategory
    """

    try:
        meta_category: MetaCategory = MetaCategory.objects.get(meetup_id=response["id"])
    except MetaCategory.DoesNotExist:
        meta_category: MetaCategory = MetaCategory.objects.create(
            meetup_id=response["id"],
            name=response["name"],
            shortname=response["shortname"],
            sort_name=response["sort_name"],
        )

    # update required fields
    meta_category.name = response["name"]
    meta_category.shortname = response["shortname"]
    meta_category.sort_name = response["sort_name"]

    # updte optional field
    if "photo" in response:
        meta_category.photo = get_photo_from_response(response["photo"])

    # update categories
    meta_category.categories.clear()
    if "category_ids" in response:
        for category_id in response["category_ids"]:
            category, created = Category.objects.get_or_create(meetup_id=category_id)
            meta_category.categories.add(category)

    meta_category.save()
    return meta_category


def get_venue_from_response(response: dict):
    """
    parse json response and return an Venue

    Keyword arguments:
    response -- meetup api response in a dict

    return -> get or create Venue
    """

    print(response)

    venue, created = Venue.objects.get_or_create(meetup_id=response["id"])
    if "address_1" in response:
        venue.address_1 = response["address_1"]
    if "address_2" in response:
        venue.address_2 = response["address_2"]
    if "address_3" in response:
        venue.address_3 = response["address_3"]
    if "city" in response:
        venue.city = response["city"]
    if "country" in response:
        venue.country = response["country"]
    if "lat" in response:
        venue.lat = response["lat"]
    if "lon" in response:
        venue.lon = response["lon"]
    if "localized_country_name" in response:
        venue.localized_country_name = response["localized_country_name"]
    if "name" in response:
        venue.name = response["name"]
    if "phone" in response:
        venue.phone = response["phone"]
    if "zip_code" in response:
        venue.zip_code = response["zip_code"]
    venue.save()
    return venue
