# Generated by Django 5.1.2 on 2024-12-18 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserPage', '0013_alter_userfavorite_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='userfavorite',
            name='src',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]