# Generated by Django 3.0.5 on 2020-05-12 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0043_auto_20200512_0623'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkedpoll',
            name='validated',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
