# Generated by Django 5.1.2 on 2024-10-23 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0012_aboutus_photographer_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='companyinfo',
            name='google_maps_link',
            field=models.URLField(blank=True, null=True),
        ),
    ]