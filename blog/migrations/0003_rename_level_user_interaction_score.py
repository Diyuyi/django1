# Generated by Django 4.2.5 on 2023-10-09 10:39

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0002_alter_categori_name"),
    ]

    operations = [
        migrations.RenameField(
            model_name="user",
            old_name="level",
            new_name="Interaction_score",
        ),
    ]
