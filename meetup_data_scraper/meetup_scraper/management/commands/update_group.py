from django.core.management.base import BaseCommand, CommandError
from meetup_data_scraper.meetup_scraper.meetup_api_client import MeetupApiClient
from meetup_data_scraper.meetup_scraper.models import GroupPage, EventPage
from meetup_data_scraper.meetup_scraper.exceptions import HttpNotFoundError


class Command(BaseCommand):
    help = "update singe group & add new past events"

    def add_arguments(self, parser):
        parser.add_argument(
            "--group_urlname",
            type=str,
            help="Meetup Group urlname wich sould be updated",
        )

        parser.add_argument(
            "--sandbox", action="store_true", help="Load the Meetup Sandbox group",
        )

    def handle(self, *args, **options):
        api_client: MeetupApiClient = MeetupApiClient()

        if options["sandbox"]:
            options["group_urlname"] = "Meetup-API-Testing"

        if not options["group_urlname"]:
            raise CommandError(
                "No group_urlname was given, add a group by --group_urlname GroupUrl or use the sandbox group by --sandbox"
            )
        try:
            group: GroupPage = api_client.get_group(options["group_urlname"])
        except HttpNotFoundError:
            raise CommandError(
                "Group with urlname {} does not exists".format(options["group_urlname"])
            )
        group_events: [EventPage] = api_client.update_all_group_events(group=group)

        print("{} has been {} events added!".format(group.name, len(group_events)))
