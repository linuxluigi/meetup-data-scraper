Getting started
=====================================

.. note::
   These instructions assume familiarity with `Docker <https://www.docker.com/>`_ and
   `Docker Compose <https://docs.docker.com/compose/>`_.

Development & Production Version
--------------------------------

The Project comes with 2 different Docker-Compose files wich are for development ``local.yml`` and production ``production.yml``.

The development version start the website in debug mode and bind the local path ``./`` to the django docker contaiers path ``/app``. 

For the production version, the docker container is build with the code inside of the container. Also the production version use redis 
as caching backend.

Quick install (Development Version)
-----------------------------------

Build the docker container.

.. code-block:: console

    $ docker-compose -f local.yml build

Create the sql tables or update the tables.

.. code-block:: console

    $ docker-compose -f local.yml run django python manage.py migrate

Create a new superuser account.

.. code-block:: console

    $ docker-compose -f local.yml run django python manage.py createsuperuser

Load the Meetup Sandbox Group with all events.

.. code-block:: console

    $ docker-compose -f local.yml run django python manage.py update_group --sandbox

Start the website.

.. code-block:: console

    $ docker-compose -f local.yml up

Now you can go to http://localhost:8000/ to visist your local site or to http://localhost:8000/admin/ to log in your admin panel.

Quick install (Production Version)
----------------------------------

Settings
^^^^^^^^ 

At first create the directory ``./.envs/.production`` 

.. code-block:: console

    $ mkdir ./.envs\.production`

For Django container create a file ``./.envs/.production/.django`` wich should look like:

.. code-block::

    # General
    # ------------------------------------------------------------------------------
    # DJANGO_READ_DOT_ENV_FILE=True
    DJANGO_SETTINGS_MODULE=config.settings.production
    DJANGO_SECRET_KEY=6Gbl8AsDbW9sgXEWrnslooEEp6iiJDOhlNd2jVFXLdLjqv7uZjaQCuxnboOOCBxl
    DJANGO_ADMIN_URL=7qW3YfapGX9k3zNVftQm/
    DJANGO_ALLOWED_HOSTS=.meetup-data-scraper.saxsys.de

    # Security
    # ------------------------------------------------------------------------------
    # TIP: better off using DNS, however, redirect is OK too
    DJANGO_SECURE_SSL_REDIRECT=False

    # Email
    # ------------------------------------------------------------------------------
    MAILGUN_API_KEY=
    DJANGO_SERVER_EMAIL=
    MAILGUN_DOMAIN=

    # Gunicorn
    # ------------------------------------------------------------------------------
    WEB_CONCURRENCY=4

    # Sentry
    # ------------------------------------------------------------------------------
    SENTRY_DSN=


    # Redis
    # ------------------------------------------------------------------------------
    REDIS_URL=redis://redis:6379/0

.. warning::
   Change DJANGO_SECRET_KEY & DJANGO_ADMIN_URL with your random strings.

   Don't share the DJANGO_SECRET_KEY with anybody!

   Share the DJANGO_ADMIN_URL only with the admins and moderators of the page! DJANGO_ADMIN_URL is the path for the admin panel,
   in this case it will be https://meetup-data-scraper.de/7qW3YfapGX9k3zNVftQm/

For Elasticsearch container create a file ``./.envs/.production/.elasticsearch`` wich should look like below. For further
information how to setup Elasticsearch with enviroment vars got to https://www.elastic.co/guide/en/elasticsearch/reference/current/settings.html

.. code-block::

    # Elasticsearch
    # ------------------------------------------------------------------------------
    http.host=elasticsearch
    http.port=9200
    node.name=elasticsearch1
    cluster.name=meetup-data-scryper-cluster
    cluster.initial_master_nodes=elasticsearch1

For Postgres container create a file ``./.envs/.production/.postgres`` wich should look like:

.. code-block::

    # PostgreSQL
    # ------------------------------------------------------------------------------
    POSTGRES_HOST=postgres
    POSTGRES_PORT=5432
    POSTGRES_DB=meetup_data_scraper
    POSTGRES_USER=rT6hv58824z9MdqKZsRw4z9MdqKZsRw
    POSTGRES_PASSWORD=SFazbAVV9W68e526Bkh3g7b5RuW8NyBzFSnm5QDwrwDf7Ty5Qsg6PAQyHQYJC94Z


Setup
^^^^^

Build the docker container.

.. code-block:: console

    $ docker-compose -f production.yml build

Create the sql tables or update the tables.

.. code-block:: console

    $ docker-compose -f production.yml run django python manage.py migrate

Create a new superuser account.

.. code-block:: console

    $ docker-compose -f production.yml run django python manage.py createsuperuser

Start the website.

.. code-block:: console

    $ docker-compose -f local.yml up -d

.. note::
    For deployment instructions visit https://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html
    
    !! There is no need to add a media storage (AWS S3 or GCP) for this project like it is described in cookiecutter-django docs !!