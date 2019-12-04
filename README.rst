Meetup Data Scraper
======================

Dowload group & events from Meetup-API into a database to make a fulltext search on every event.

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
     :target: https://github.com/ambv/black
     :alt: Black code style
.. image:: https://travis-ci.com/linuxluigi/meetup-data-scraper.svg?branch=master
     :target: https://travis-ci.com/linuxluigi/meetup-data-scraper
     :alt: Travis CI tests
.. image:: https://readthedocs.org/projects/meetup-data-scraper/badge/?version=latest
     :target: https://meetup-data-scraper.readthedocs.io/en/latest/?badge=latest
     :alt: Documentation Status
.. image:: https://coveralls.io/repos/github/linuxluigi/meetup-data-scraper/badge.svg?branch=master
     :target: https://coveralls.io/github/linuxluigi/meetup-data-scraper?branch=master
     :alt: Coverage


Settings
--------

Moved to settings_.

.. _settings: http://cookiecutter-django.readthedocs.io/en/latest/settings.html

Basic Commands
--------------

Setting Up Your Users
^^^^^^^^^^^^^^^^^^^^^

* To create an **superuser account**, use this command::

    $ docker-compose -f local.yml run django python manage.py createsuperuser

Type checks
^^^^^^^^^^^

Running type checks with mypy:

::

  $ docker-compose -f local.yml run django coverage run -m mypy meetup_data_scraper

Test coverage
^^^^^^^^^^^^^

To run the tests, check your test coverage, and generate an HTML coverage report::

    $ docker-compose -f local.yml run django coverage run -m pytest
    $ docker-compose -f local.yml run django coverage run -m coverage html
    $ open htmlcov/index.html

Running tests with py.test
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  $ docker-compose -f local.yml run django coverage run -m pytest





Sentry
^^^^^^

Sentry is an error logging aggregator service. You can sign up for a free account at  https://sentry.io/signup/?code=cookiecutter  or download and host it yourself.
The system is setup with reasonable defaults, including 404 logging and integration with the WSGI application.

You must set the DSN url in production.


Deployment
----------

The following details how to deploy this application.


Heroku
^^^^^^

See detailed `cookiecutter-django Heroku documentation`_.

.. _`cookiecutter-django Heroku documentation`: http://cookiecutter-django.readthedocs.io/en/latest/deployment-on-heroku.html



Docker
^^^^^^

See detailed `cookiecutter-django Docker documentation`_.

.. _`cookiecutter-django Docker documentation`: http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html



