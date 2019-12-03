import requests
from .exceptions import (
    HttpNoSuccess,
    HttpNotFoundError,
    HttpNotAccessibleError,
    HttpNoXRateLimitHeader,
)
import time
from .models import HomePage, GroupPage, EventPage
from requests.models import Response
from django.utils import timezone
import pytz
from datetime import datetime


timezone.activate(pytz.timezone("UTC"))


class RateLimit:
    """
    meetup api rate limit, wait for new request if needed
    """

    #

    def __init__(self):
        super().__init__()

        # The maximum number of requests that can be made in a window of time
        self.limit: int = 0

        # The remaining number of requests allowed in the current rate limit window
        self.remaining: int = 0

        # The number of seconds until the current rate limit window resets
        self.reset: int = 0

        # unixtime when limits will be reseted
        self.reset_time: float = None

    def wait_for_next_request(self):
        """
        wait for next request, if needed
        """
        if not self.reset_time:
            return

        if self.remaining < 1:
            while self.reset_time > time.time():
                time.sleep(1)

    def update_rate_limit(self, response: Response):
        """
        Update rate limit information from response header

        Keyword arguments:
        response -- http response
        """
        try:
            self.limit = int(response.headers.get("X-RateLimit-Limit"))
            self.remaining = int(response.headers.get("X-RateLimit-Remaining"))
            self.reset = int(response.headers.get("X-RateLimit-Reset"))
            self.reset_time = time.time() + self.reset
        except TypeError:
            self.limit = 0
            self.remaining = 0
            self.reset = 60
            self.reset_time = time.time() + self.reset
            raise HttpNoXRateLimitHeader("A very specific bad thing happened.")


class MeetupApiClient:
    """
    small meetup api client only for groups & events
    """

    def __init__(self):
        super().__init__()
        self.rate_limit = RateLimit()

        # meetup apir url
        self.base_url: str = "https://api.meetup.com/"

        # default homepage, page will created automatically on migrate
        self.home_page: HomePage = None

    def get_home_page(self) -> HomePage:
        """
        get the default homepage wich will created on migration

        return -> default HomePage
        """
        if not self.home_page:
            self.homePage = HomePage.objects.all()[:1].get()
        return self.homePage

    def get(self, url_path: str, retry: int = 0, max_retry=3) -> dict:
        """
        meetup http request on the url_path

        Keyword arguments:
        url_path -- url path without domain example for url https://api.meetup.com/find/groups is the url_path find/groups
        retry -- how many times try to get the same url
        max_retry -- max retries bevor raise an error

        return -> json as python dict
        """
        self.rate_limit.wait_for_next_request()

        url: str = "{}{}".format(self.base_url, url_path)
        response: Response = requests.get(url)

        if response.status_code == 404:
            raise HttpNotFoundError
        if response.status_code == 410:
            raise HttpNotAccessibleError
        if response.status_code != 200:
            if retry <= max_retry:
                raise HttpNoSuccess
            else:
                return self.get(url_path=url_path, retry=retry + 1)

        try:
            self.rate_limit.update_rate_limit(response=response)
        except HttpNoXRateLimitHeader:
            if retry <= max_retry:
                raise HttpNoXRateLimitHeader
            else:
                return self.get(url_path=url_path, retry=retry + 1)

        return response.json()

    def get_group(self, group_urlname: str) -> GroupPage:
        """
        get or create a GroupPage based on the group_urlname and fill / update the object from meetup rest api

        Keyword arguments:
        group_urlname -- Meetup group the urlname as string

        return -> GroupPage based on the group_urlname
        """
        try:
            response: dict = self.get("{}".format(group_urlname))
        except (HttpNotFoundError, HttpNotAccessibleError) as e:

            # delete group if exists
            try:
                group: GroupPage = GroupPage.objects.get(urlname=group_urlname)
                group.delete()
            except GroupPage.DoesNotExist:
                pass

            print(e)
            return

        except (HttpNoSuccess, HttpNoXRateLimitHeader) as e:
            print(e)
            return

        try:
            group: GroupPage = GroupPage.objects.get(urlname=group_urlname)
            group.status = response["status"]
            group.description = response["description"]
            group.city = response["city"]
            group.country = response["country"]
            group.lat = response["lat"]
            group.lon = response["lon"]
            group.members = response["members"]
            group.member_pay_fee = response["member_pay_fee"]
            group.save()

        except GroupPage.DoesNotExist:
            group: GroupPage = GroupPage(
                meetup_id=response["id"],
                title="{}: {}".format(response["id"], response["name"]),
                name=response["name"],
                urlname=group_urlname,
                slug=response["id"],
                status=response["status"],
                description=response["description"],
                created=timezone.make_aware(
                    datetime.fromtimestamp(response["created"] / 1000)
                ),
                city=response["city"],
                country=response["country"],
                lat=response["lat"],
                lon=response["lon"],
                members=response["members"],
            )
            self.get_home_page().add_child(instance=group)
            group.save_revision().publish()

        return group

    def update_all_group_events(
        self, group: GroupPage, max_entries_per_page: int = 200
    ) -> [EventPage]:
        """
        get all past events from meetup rest api & add it as child pages to the group

        Keyword arguments:
        group -- GroupPage
        max_entries_per_page -- how much events get from the meetup rest api per request (default 200, min 1, max 200)

        return -> [EventPage] every new Events wich wasn't in the database
        """

        # set max_entries_per_page between 1 to 200
        if max_entries_per_page < 1:
            max_entries_per_page = 1
        if max_entries_per_page > 200:
            max_entries_per_page = 200

        # meetup rest api page offset
        offset_counter: int = 0

        # return [EventPage], init empty
        events: [EventPage] = []

        # fetch all events
        while True:
            group_events: [EventPage] = self.update_group_events(
                group=group, max_entries=max_entries_per_page, offset=offset_counter
            )
            events.extend(group_events)
            if len(group_events) < 200:
                break
            offset_counter = offset_counter + 1

        return events

    def update_group_events(
        self, group: GroupPage, max_entries: int = 200, offset: int = 0
    ) -> [EventPage]:
        """
        get new past events from meetup rest api & add it as child pages to the group

        Keyword arguments:
        group -- GroupPage
        max_entries_per_page -- how much events get from the meetup rest api per request (default 200, min 1, max 200)
        offset -- meetup page offset (default 0, min 0)

        return -> [EventPage] new Events wich wasn't in the database from the request
        """

        # set offset to min value
        if offset < 0:
            offset = 0

        # get last event from group
        last_event: EventPage = group.last_event()

        # return [EventPage], init empty
        events: [EventPage] = []

        # when there is a last event -> set on meetup that only events fetch wich are no ealier than this event

        try:
            if last_event:
                response: dict = self.get(
                    "{}/events?status=past&no_earlier_than={}&page={}&offset={}".format(
                        group.urlname,
                        last_event.time.strftime("%Y-%m-%d"),
                        max_entries,
                        offset,
                    )
                )
            else:
                response: dict = self.get(
                    "{}/events?status=past&page={}&offset={}".format(
                        group.urlname, max_entries, offset
                    )
                )
        except (
            HttpNotFoundError,
            HttpNotAccessibleError,
            HttpNoSuccess,
            HttpNoXRateLimitHeader,
        ) as e:
            print(e)
            return events

        # go through every event from response and at them to the database
        for event_response in response:
            try:
                EventPage.objects.get(meetup_id=event_response["id"])
            except EventPage.DoesNotExist:

                try:
                    description = event_response["description"]
                except KeyError:
                    description = ""

                try:
                    status = event_response["status"]
                except KeyError:
                    status = ""

                event: EventPage = EventPage(
                    meetup_id=str(event_response["id"]),
                    title="{}: {}".format(event_response["id"], event_response["name"]),
                    name=event_response["name"],
                    slug=event_response["id"],
                    status=status,
                    time=timezone.make_aware(
                        datetime.fromtimestamp(event_response["time"] / 1000)
                    ),
                    description=description,
                )
                group.add_child(instance=event)
                event.save_revision().publish()
                events.append(event)
            except KeyError:
                pass

        return events
