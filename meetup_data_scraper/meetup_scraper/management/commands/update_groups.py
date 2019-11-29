from django.core.management.base import BaseCommand
from meetup_data_scraper.meetup_scraper.meetup_api_client import MeetupApiClient
from meetup_data_scraper.meetup_scraper.models import GroupPage, EventPage


class Command(BaseCommand):
    help = "Update all groups from Meetup Rest & add every new event fro groups"

    def handle(self, *args, **options):
        api_client: MeetupApiClient = MeetupApiClient()
        group: GroupPage = api_client.get_group("Meetup-API-Testing")

        groups: [GroupPage] = GroupPage.objects.all()
        event_counter: int = 0

        for group in groups:
            group_events: [EventPage] = api_client.update_all_group_events(group=group)
            event_counter = event_counter + len(group_events)

        print(
            "{} groups was updated & {} events added".format(len(groups), event_counter)
        )
