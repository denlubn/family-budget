# Generated by Django 4.1.3 on 2022-11-03 13:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("budget", "0002_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="budget",
            options={"ordering": ["id"]},
        ),
    ]
