Usage Guide
=====================================

CLI
---

get_groups
^^^^^^^^^^ 

Load mutiple groups from JSON files. The JSON files muss include a key & a URL name. To download use the rest api direkt or via
the meetup website https://secure.meetup.com/meetup_api/console/?path=/find/groups 

An example Rest API request for the first 200 german groups -> https://api.meetup.com/find/groups?&sign=true&photo-host=public&country=DE&page=200&offset=0&only=urlname

After you downloaded the json, put them into ``./meetup_data_scraper``. When you download the JSON's in a another directory set the path via
``--json_path /app/your-dir/``. When you run the command in docker, you need to set the path inside the docker container.

.. code-block:: console

    $ docker-compose -f local.yml run django python manage.py get_groups

Example JSON file in ``./compose/local/django/meetup_groups/test-groups.json``

.. literalinclude:: ../compose/local/django/meetup_groups/test-groups.json
    :language: json


update_group
^^^^^^^^^^^^

Load a single group with all events from meetup rest api. When the group already exist in the database,
it will just update the group and load new events to the group.

To set a group, use the param ``--group_urlname GROUP_URLNAME``, for load the meetup sandbox group use:

.. code-block:: console

    $ docker-compose -f local.yml run django python manage.py update_group --group_urlname Meetup-API-Testing

Or as a special case to load the sandbox group, add the param ``--sandbox`` without a value:

.. code-block:: console

    $ docker-compose -f local.yml run django python manage.py update_group --sandbox

update_groups
^^^^^^^^^^^^^

To get all new events from all groups in the database use:

.. code-block:: console

    $ docker-compose -f local.yml run django python manage.py update_groups