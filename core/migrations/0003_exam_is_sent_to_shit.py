# Generated by Django 2.2.1 on 2019-06-07 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20190608_0016'),
    ]

    operations = [
        migrations.AddField(
            model_name='exam',
            name='is_sent_to_shit',
            field=models.BooleanField(default=False),
        ),
    ]
