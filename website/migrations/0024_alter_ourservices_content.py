# Generated by Django 5.1.2 on 2024-10-26 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0023_ourservices_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ourservices',
            name='content',
            field=models.TextField(blank=True, null=True),
        ),
    ]
