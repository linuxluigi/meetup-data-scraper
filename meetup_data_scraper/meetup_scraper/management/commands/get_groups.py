from django.core.management.base import BaseCommand
from meetup_data_scraper.meetup_scraper.meetup_api_client import MeetupApiClient
from meetup_data_scraper.meetup_scraper.models import GroupPage, EventPage
import json
import glob


class Command(BaseCommand):
    help = "load all groups from json files stored in /meetup_groups/*.json"

    def handle(self, *args, **options):
        api_client: MeetupApiClient = MeetupApiClient()

        # json generated on https://api.meetup.com/find/groups?&sign=true&photo-host=public&country=DE&page=200&offset=0&only=urlname
        mettup_groups_files: [] = glob.glob("/app/meetup_groups/*.json")

        group_counter: int = 0
        event_counter: int = 0

        for mettup_groups_file in mettup_groups_files:
            with open(mettup_groups_file) as json_file:
                data = json.load(json_file)

                group_counter = group_counter + len(data)

                for group_data in data:
                    group: GroupPage = api_client.get_group(data[group_data]["urlname"])
                    group_events: [EventPage] = api_client.update_all_group_events(
                        group=group
                    )

                    event_counter = event_counter + len(group_events)

                    print(
                        "Group {} was updatet with {} events".format(
                            group.name, len(group_events)
                        )
                    )

        print(
            "{} groups was updatet with {} new events".format(
                group_counter, event_counter
            )
        )
