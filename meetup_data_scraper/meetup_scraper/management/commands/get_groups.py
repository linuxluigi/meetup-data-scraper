from django.core.management.base import BaseCommand
from meetup_data_scraper.meetup_scraper.meetup_api_client.meetup_api_client import (
    MeetupApiClient,
)
from meetup_data_scraper.meetup_scraper.models import GroupPage, EventPage
import json
import glob


class Command(BaseCommand):
    help = "load all groups from json files stored in /meetup_groups/*.json"

    def add_arguments(self, parser):
        parser.add_argument(
            "--json_path", type=str, help="Path of the meetup groups jsons",
        )

    def handle(self, *args, **options):
        api_client: MeetupApiClient = MeetupApiClient()

        if not options["json_path"]:
            options["json_path"] = "/app/meetup_groups"

        mettup_groups_files: [] = glob.glob("{}/*.json".format(options["json_path"]))

        group_counter: int = 0
        group_not_exists_counter: int = 0
        event_counter: int = 0

        for mettup_groups_file in mettup_groups_files:
            with open(mettup_groups_file) as json_file:
                data = json.load(json_file)

                for group_data in data:
                    group: GroupPage = api_client.get_group(data[group_data]["urlname"])

                    #  break if group not exists
                    if not group:
                        group_not_exists_counter = group_not_exists_counter + 1
                        break
                    group_counter = group_counter + 1

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
            "{} groups was updatet with {} new events & {} do not exists anymore".format(
                group_counter, event_counter, group_not_exists_counter
            )
        )
