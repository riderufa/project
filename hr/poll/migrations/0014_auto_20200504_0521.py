# Generated by Django 3.0.5 on 2020-05-04 05:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0013_auto_20200504_0519'),
    ]

    operations = [
        migrations.AddField(
            model_name='poll',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_polls', to='poll.UserProfile', verbose_name='пользователь'),
        ),
        migrations.AlterField(
            model_name='poll',
            name='admin',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='admin_polls', to='poll.UserProfile', verbose_name='администратор'),
        ),
    ]
