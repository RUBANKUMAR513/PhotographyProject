# Generated by Django 5.1.2 on 2024-10-26 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0025_rename_ourservices_ourservice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ourservice',
            name='orientation',
            field=models.CharField(choices=[('right', 'Right'), ('left', 'Left')], default='left', help_text='Align image Container', max_length=10),
        ),
    ]
