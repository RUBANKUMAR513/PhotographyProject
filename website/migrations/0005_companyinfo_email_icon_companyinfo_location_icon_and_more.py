# Generated by Django 5.1.2 on 2024-10-22 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_companyinfo_facebook_icon_companyinfo_instagram_icon_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='companyinfo',
            name='email_icon',
            field=models.ImageField(blank=True, default='default_email_icon.png', null=True, upload_to='icons/'),
        ),
        migrations.AddField(
            model_name='companyinfo',
            name='location_icon',
            field=models.ImageField(blank=True, default='default_location_icon.png', null=True, upload_to='icons/'),
        ),
        migrations.AddField(
            model_name='companyinfo',
            name='phone_icon',
            field=models.ImageField(blank=True, default='default_phone_icon.png', null=True, upload_to='icons/'),
        ),
    ]