# Generated by Django 4.2.5 on 2023-09-15 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('code_feed', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='codemodel',
            name='created_at',
            field=models.DateTimeField(),
        ),
    ]