# Generated by Django 3.0.5 on 2020-05-10 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0036_auto_20200510_0526'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='checkedpoll',
            name='rank',
        ),
        migrations.AddField(
            model_name='checkedquestion',
            name='rank',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
