# Generated by Django 2.2.7 on 2019-11-28 09:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailcore", "0041_group_collection_permissions_verbose_name_plural"),
        ("meetup_scraper", "0002_create_homepage"),
    ]

    operations = [
        migrations.CreateModel(
            name="EventPage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.Page",
                    ),
                ),
                ("meetup_id", models.CharField(max_length=255, unique=True)),
                ("name", models.CharField(max_length=100)),
                ("status", models.CharField(blank=True, max_length=100, null=True)),
                ("time", models.DateTimeField()),
                ("description", models.TextField(blank=True, null=True)),
            ],
            options={"abstract": False,},
            bases=("wagtailcore.page",),
        ),
        migrations.CreateModel(
            name="GroupPage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.Page",
                    ),
                ),
                ("meetup_id", models.BigIntegerField(unique=True)),
                ("name", models.CharField(max_length=100)),
                ("status", models.CharField(max_length=100)),
                ("urlname", models.CharField(max_length=100, unique=True)),
                ("description", models.TextField()),
                ("created", models.DateTimeField()),
                ("city", models.CharField(max_length=100)),
                ("country", models.CharField(max_length=5)),
                ("lat", models.DecimalField(decimal_places=8, max_digits=10)),
                ("lon", models.DecimalField(decimal_places=8, max_digits=10)),
                ("members", models.IntegerField()),
            ],
            options={"abstract": False,},
            bases=("wagtailcore.page",),
        ),
    ]
