# Generated by Django 5.1.2 on 2024-10-25 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0020_babypropsimage_enable'),
    ]

    operations = [
        migrations.AddField(
            model_name='companyinfo',
            name='babyProps_header_logo',
            field=models.ImageField(default='default_logo.png', upload_to='logos/'),
        ),
    ]
