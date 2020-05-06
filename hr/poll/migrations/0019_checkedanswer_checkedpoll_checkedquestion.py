# Generated by Django 3.0.5 on 2020-05-05 12:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0018_auto_20200505_0821'),
    ]

    operations = [
        migrations.CreateModel(
            name='CheckedPoll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('admin', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='admin_checked_polls', to='poll.UserProfile', verbose_name='администратор')),
                ('poll', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='poll.Poll')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_checked_polls', to='poll.UserProfile', verbose_name='пользователь')),
            ],
        ),
        migrations.CreateModel(
            name='CheckedQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='poll.CheckedPoll')),
                ('question', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='poll.Question', verbose_name='вопрос')),
            ],
        ),
        migrations.CreateModel(
            name='CheckedAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='текст ответа')),
                ('checked', models.BooleanField(verbose_name='валидность ответа')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='poll.CheckedQuestion')),
            ],
        ),
    ]