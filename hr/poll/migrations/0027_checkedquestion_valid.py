# Generated by Django 3.0.5 on 2020-05-09 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0026_auto_20200509_0616'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkedquestion',
            name='valid',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
