# Generated by Django 3.0.5 on 2020-05-09 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0034_auto_20200509_1825'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkedpoll',
            name='rank',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
