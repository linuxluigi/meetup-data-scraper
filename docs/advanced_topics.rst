Advanced topics
=====================================

Changing Models
---------------

The models in ``.meetup_data_scraper/meetup_scraper/models.py`` are pages based on `Wagtail CMS <https://wagtail.io>`_. 
For further information how to change the models read the docs from `Wagtail Doc - Page Models <https://docs.wagtail.io/en/v2.7/topics/pages.html>`_

The hierarchy strukture of the page models is:

``HomePage`` -> ``GroupPage`` -> ``EventPage``

The default ``HomePage`` will automatically created on the first ``migrate`` process. The HomePage will only accept GroupPages as child and the GroupPages
accept only EventPages.

