# Generated by Django 4.2 on 2023-07-24 09:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("useraccount", "0002_alter_user_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="is_user",
            field=models.BooleanField(default=True),
        ),
    ]
