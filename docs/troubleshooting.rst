Troubleshooting
=====================================

This page contains some advice about errors and problems commonly encountered during the development of Meetup Data Scraper.


max virtual memory areas vm.max_map_count [65530] likely too low, increase to at least [262144]
-----------------------------------------------------------------------------------------------

When using docker on some machines, you will need to manually extend the max virtual memory. For CentOS & Ubuntu use::

    $ sudo sysctl -w vm.max_map_count=262144

Test faild
----------

In some cases the tests can fail cause of a coruppted database. Try to reset your test database und retry the test.