# Generated by Django 3.0.5 on 2020-05-04 05:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0012_auto_20200503_0933'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='poll',
            name='user',
        ),
        migrations.AddField(
            model_name='poll',
            name='admin',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='user_polls', to='poll.UserProfile', verbose_name='администратор'),
        ),
    ]
