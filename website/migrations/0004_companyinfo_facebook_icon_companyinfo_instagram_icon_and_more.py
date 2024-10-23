# Generated by Django 5.1.2 on 2024-10-22 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_companyinfo_enable_tagline_companyinfo_tagline'),
    ]

    operations = [
        migrations.AddField(
            model_name='companyinfo',
            name='facebook_icon',
            field=models.ImageField(blank=True, default='default_facebook_icon.png', null=True, upload_to='icons/'),
        ),
        migrations.AddField(
            model_name='companyinfo',
            name='instagram_icon',
            field=models.ImageField(blank=True, default='default_instagram_icon.png', null=True, upload_to='icons/'),
        ),
        migrations.AddField(
            model_name='companyinfo',
            name='whatsapp_icon',
            field=models.ImageField(blank=True, default='default_whatsapp_icon.png', null=True, upload_to='icons/'),
        ),
        migrations.AddField(
            model_name='companyinfo',
            name='x_icon',
            field=models.ImageField(blank=True, default='default_x_icon.png', null=True, upload_to='icons/'),
        ),
        migrations.AddField(
            model_name='companyinfo',
            name='youtube_icon',
            field=models.ImageField(blank=True, default='default_youtube_icon.png', null=True, upload_to='icons/'),
        ),
    ]