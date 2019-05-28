# Generated by Django 2.2.1 on 2019-05-28 13:03

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exam',
            name='end_datetime',
        ),
        migrations.RemoveField(
            model_name='exam',
            name='start_datetime',
        ),
        migrations.AddField(
            model_name='exam',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='exam',
            name='end_at',
            field=models.TimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='exam',
            name='start_at',
            field=models.TimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
