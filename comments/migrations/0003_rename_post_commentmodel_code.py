# Generated by Django 4.2.5 on 2023-09-14 11:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0002_alter_commentmodel_created_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='commentmodel',
            old_name='post',
            new_name='code',
        ),
    ]
