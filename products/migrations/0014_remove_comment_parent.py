# Generated by Django 4.2 on 2023-06-16 12:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0013_comment_parent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='parent',
        ),
    ]