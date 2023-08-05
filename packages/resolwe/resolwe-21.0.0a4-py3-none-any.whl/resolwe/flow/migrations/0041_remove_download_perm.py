# Generated by Django 2.2.6 on 2019-10-28 10:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("flow", "0040_remove_entity_descriptor_completed"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="collection",
            options={
                "default_permissions": (),
                "get_latest_by": "version",
                "permissions": (
                    ("view_collection", "Can view collection"),
                    ("edit_collection", "Can edit collection"),
                    ("share_collection", "Can share collection"),
                    ("owner_collection", "Is owner of the collection"),
                ),
            },
        ),
        migrations.AlterModelOptions(
            name="data",
            options={
                "default_permissions": (),
                "get_latest_by": "version",
                "permissions": (
                    ("view_data", "Can view data"),
                    ("edit_data", "Can edit data"),
                    ("share_data", "Can share data"),
                    ("owner_data", "Is owner of the data"),
                ),
            },
        ),
        migrations.AlterModelOptions(
            name="entity",
            options={
                "default_permissions": (),
                "get_latest_by": "version",
                "permissions": (
                    ("view_entity", "Can view entity"),
                    ("edit_entity", "Can edit entity"),
                    ("share_entity", "Can share entity"),
                    ("owner_entity", "Is owner of the entity"),
                ),
            },
        ),
    ]
