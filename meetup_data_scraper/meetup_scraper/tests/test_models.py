import pytest
from .factories import (
    GroupPageFactory,
    EventPage1Factory,
    EventPage2Factory,
    EventPage3Factory,
)

pytestmark = pytest.mark.django_db


def test_group_page_last_event():
    # test when there is no event
    sandbox_group = GroupPageFactory()
    assert sandbox_group.last_event() is None

    # test when there is a new event
    sandbox_event_1 = EventPage1Factory()
    assert sandbox_group.last_event().meetup_id == sandbox_event_1.meetup_id

    sandbox_event_2 = EventPage2Factory()
    EventPage3Factory()
    assert sandbox_group.last_event().meetup_id == sandbox_event_2.meetup_id


def test_group_page_events():
    # test when there is no event
    sandbox_group = GroupPageFactory()
    assert len(sandbox_group.events()) == 0

    # add one event
    EventPage1Factory()
    assert len(sandbox_group.events()) == 1

    # add tow events
    EventPage2Factory()
    EventPage3Factory()
    assert len(sandbox_group.events()) == 3
