# Generated by Django 3.0.5 on 2020-05-02 08:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0002_userprofile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='answers_question',
            new_name='answers',
        ),
        migrations.RenameField(
            model_name='question',
            old_name='image_question',
            new_name='image',
        ),
        migrations.RenameField(
            model_name='question',
            old_name='text_question',
            new_name='text',
        ),
        migrations.RenameField(
            model_name='question',
            old_name='time_limit_question',
            new_name='time_limit',
        ),
        migrations.RenameField(
            model_name='question',
            old_name='type_question',
            new_name='type',
        ),
    ]
