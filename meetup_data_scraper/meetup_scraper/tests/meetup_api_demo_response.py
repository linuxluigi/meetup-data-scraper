def get_photo_response(
    meetup_id: int = 1, photo_type: str = "event", content: bool = False
) -> dict:
    """
    create a Photo response

    Keyword arguments:
    meetup_id -- meetup id
    photo_type -- event or member 
    content -- if True -> add optional fields

    return -> photo dict
    """

    response: dict = {
        "id": meetup_id,
    }

    if content:

        content_response: dict = {
            "highres_link": "https://secure.meetupstatic.com/photos/event/2/b/c/a/highres_{}.jpeg".format(
                meetup_id
            ),
            "photo_link": "https://secure.meetupstatic.com/photos/event/2/b/c/a/600_{}.jpeg".format(
                meetup_id
            ),
            "thumb_link": "https://secure.meetupstatic.com/photos/event/2/b/c/a/thumb_{}.jpeg".format(
                meetup_id
            ),
            "type": photo_type,
            "base_url": "https://secure.meetupstatic.com",
        }

        return {**response, **content_response}

    return response


def get_member_response(meetup_id: int = 1, content: bool = False) -> dict:
    """
    create a Member response

    Keyword arguments:
    meetup_id -- meetup id
    content -- if True -> add optional fields

    return -> member dict
    """

    response: dict = {
        "id": meetup_id,
    }

    if content:

        content_response: dict = {
            "name": "Max",
            "bio": "you don't get better",
            "photo": get_photo_response(
                meetup_id=321, photo_type="member", content=True
            ),
        }

        return {**response, **content_response}

    return response


def get_category_response(meetup_id: int = 34, content: bool = False) -> dict:
    """
    create a Category response

    Keyword arguments:
    meetup_id -- meetup id
    content -- if True -> add optional fields

    return -> category dict
    """

    response: dict = {
        "id": meetup_id,
    }

    if content:

        content_response: dict = {
            "name": "Tech",
            "shortname": "tech",
            "sort_name": "Tech",
        }

        return {**response, **content_response}

    return response


def get_meta_category_response(meetup_id: int = 252, content: bool = False) -> dict:
    """
    create a MetaCategory response

    Keyword arguments:
    meetup_id -- meetup id
    content -- if True -> add optional fields

    return -> meta category dict
    """

    response: dict = {
        "id": meetup_id,
        "shortname": "tech",
        "name": "Tech",
        "sort_name": "Tech",
    }

    if content:

        content_response: dict = {
            "photo": get_photo_response(),
            "category_ids": [get_category_response()["id"]],
        }

        return {**response, **content_response}

    return response


def get_fee_options_response(
    content_currencies: bool = False, content_currencies_default: bool = False
) -> dict:
    """
    create a fee_options response for group

    Keyword arguments:
    content_currencies -- if True -> add optional field currencies
    content_currencies_default -- if True -> add optional field default in currencies

    return -> category dict
    """

    response: dict = {
        "currencies": {"code": "EUR", "default": True},
        "type": "cash",
    }

    if content_currencies:
        content_response: dict = {
            "currencies": {"code": "EUR"},
        }
        if content_currencies_default:
            content_response["currencies"]["default"] = True

        return {**response, **content_response}

    return response


def get_topic_response(meetup_id: int = 132) -> dict:
    """
    create a Topic response

    Keyword arguments:
    meetup_id -- meetup id

    return -> topic dict
    """

    response: dict = {"id": meetup_id, "lang": "en", "name": "demo", "urlkey": "demo"}

    return response


def get_venue_response(meetup_id: int = 1, content: bool = False) -> dict:
    """
    create a Venue response

    Keyword arguments:
    meetup_id -- meetup id
    content -- if True -> add optional fields

    return -> venu dict
    """

    response: dict = {
        "id": meetup_id,
    }

    if content:

        content_response: dict = {
            "address_1": "Berlinerstr. 1",
            "address_2": "oben",
            "address_3": "unten",
            "city": "Berlin",
            "country": "Germany",
            "lat": 52.520008,
            "lon": 13.404954,
            "localized_country_name": "Deutschland",
            "name": "Meetup Place",
            "phone": "030 123 456 789",
            "zip_code": "10101",
        }

        return {**response, **content_response}

    return response


def get_event_host_response(content: bool = False) -> dict:
    """
    create a EventHost response

    Keyword arguments:
    content -- if True -> add optional fields

    return -> event host dict
    """

    response: dict = {}

    if content:

        content_response: dict = {
            "host_count": 10,
            "id": get_member_response()["id"],
            "intro": "I'm host",
            "join_date": 1560639600000,
            "name": "Hosti",
            "photo": get_photo_response(),
        }

        return {**response, **content_response}

    return response


def get_group_response(
    meetup_id: int = 1, urlname: str = "Meetup-API-Testing", content: bool = False
) -> dict:
    """
    create a Group response

    Keyword arguments:
    meetup_id -- meetup id
    urlname -- meetup urlname
    content -- if True -> add optional fields

    return -> group dict
    """

    response: dict = {
        "id": meetup_id,
        "urlname": urlname,
        "created": 1258123610000,
        "description": "description",
        "lat": 40.7,
        "lon": -73.99,
        "link": "https://www.meetup.com/de-DE/Meetup-API-Testing/",
        "members": 7737,
        "name": "Meetup API Testing Sandbox",
        "status": "active",
        "timezone": "US/Eastern",
        "visibility": "public_limited",
    }

    if content:
        content_response: dict = {
            "short_link": "https://mee.up/test",
            "welcome_message": "Welcome!",
            "city": "Brooklyn",
            "city_link": "https://www.meetup.com/city/Brooklyn/",
            "untranslated_city": "Brooklyn",
            "country": "US",
            "localized_country_name": "USA",
            "localized_location": "Brooklyn, NY",
            "state": "NY",
            "join_mode": "open",
            "fee_options": get_fee_options_response(
                content_currencies=True, content_currencies_default=True
            ),
            "member_limit": 10,
            "nomination_acceptable": True,
            "organizer": get_member_response(),
            "who": "Developers",
            "group_photo": get_photo_response(),
            "key_photo": get_photo_response(),
            "category": get_category_response(),
            "topics": [get_topic_response()],
            "meta_category": get_meta_category_response(),
        }
        return {**response, **content_response}

    return response


def get_event_response(meetup_id: str = "1", content: bool = False) -> dict:
    """
    create a Event response

    Keyword arguments:
    meetup_id -- meetup id
    content -- if True -> add optional fields

    return -> event dict
    """

    response: dict = {
        "id": meetup_id,
        "name": "test meetup",
        "time": 1560639600000,
        "link": "http://localhost/",
    }

    if content:
        content_response: dict = {
            "attendance_count": 10,
            "attendance_sample": 10,
            "attendee_sample": 10,
            "created": 1560639600000,
            "date_in_series_pattern": True,
            "description": "Test Event",
            "duration": 7200000,
            "event_hosts": [get_event_host_response()],
            "fee": {
                "accepts": "cash",
                "amount": 10,
                "currency": "EUR",
                "description": "per-person",
                "label": "Price",
            },
            "how_to_find_us": "when nothing goes right, go left",
            "status": "past",
            "updated": 1560639600000,
            "utc_offset": -14400000,
            "venue": get_venue_response(),
            "venue_visibility": "public",
            "visibility": "public_limited",
        }
        return {**response, **content_response}

    return response
