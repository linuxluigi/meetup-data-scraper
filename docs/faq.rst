FAQ
===

.. index:: FAQ

What are the minimum hardware requirements?
-------------------------------------------

To host it with docker you will need at leat a vServer with 2GB RAM, 10GB disk space & 1 CPU.

How to set the domain for a production site?
--------------------------------------------

Change in ``.envs/.production/.django`` the value of ``DJANGO_ALLOWED_HOSTS`` to your domain. 
Also replace in ``compose\production\traefik\traefik.toml`` the entry ``meetup-data-scraper.de`` with your target domain.