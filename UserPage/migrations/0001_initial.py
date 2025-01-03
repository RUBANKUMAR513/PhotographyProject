# Generated by Django 5.1.2 on 2024-10-25 12:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_shoots', models.DateField()),
                ('description', models.TextField(blank=True, null=True)),
                ('allow_to_download', models.BooleanField(default=False)),
                ('remove_on', models.DateTimeField()),
                ('remaining_days', models.IntegerField(editable=False)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
