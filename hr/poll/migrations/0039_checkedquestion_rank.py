# Generated by Django 3.0.5 on 2020-05-10 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0038_remove_checkedquestion_rank'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkedquestion',
            name='rank',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
