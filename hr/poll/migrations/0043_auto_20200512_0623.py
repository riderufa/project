# Generated by Django 3.0.5 on 2020-05-12 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0042_auto_20200510_1910'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkedpoll',
            name='validated',
            field=models.IntegerField(blank=True, default=False, null=True),
        ),
    ]
