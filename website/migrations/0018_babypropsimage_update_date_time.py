# Generated by Django 5.1.2 on 2024-10-24 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0017_babypropsgallery_orientation'),
    ]

    operations = [
        migrations.AddField(
            model_name='babypropsimage',
            name='update_date_time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
