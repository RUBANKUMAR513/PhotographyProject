# Generated by Django 5.1.2 on 2024-10-23 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0014_companyinfo_gif_duration_companyinfo_intro_gif'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyinfo',
            name='gif_duration',
            field=models.FloatField(blank=True, help_text='In Seconds', null=True),
        ),
    ]
