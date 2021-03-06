# Generated by Django 3.0.5 on 2020-05-02 09:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0003_auto_20200502_0803'),
    ]

    operations = [
        migrations.CreateModel(
            name='Kit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.IntegerField()),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poll.Question')),
            ],
        ),
        migrations.CreateModel(
            name='QuestionList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='наименование опроса')),
                ('time_limit', models.IntegerField(blank=True, null=True, verbose_name='предельное время (сек)')),
                ('date_pub', models.DateField(verbose_name='дата публикации')),
                ('questions', models.ManyToManyField(related_name='question_lists', through='poll.Kit', to='poll.Question')),
            ],
        ),
        migrations.AddField(
            model_name='kit',
            name='questionlist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poll.QuestionList'),
        ),
    ]
