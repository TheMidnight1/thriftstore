# Generated by Django 4.2 on 2023-05-25 03:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_rename_created_at_comment_timestamp_comment_parent'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='timestamp',
            new_name='created_at',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='parent',
        ),
    ]