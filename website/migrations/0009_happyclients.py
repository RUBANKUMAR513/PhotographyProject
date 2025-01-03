# Generated by Django 5.1.2 on 2024-10-23 05:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0008_homepagegallery'),
    ]

    operations = [
        migrations.CreateModel(
            name='HappyClients',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reviews', models.TextField(help_text="Client's review", max_length=1000)),
                ('client_name', models.CharField(help_text="Client's name", max_length=255)),
                ('image', models.ImageField(help_text="Client's image", upload_to='clients/')),
                ('cartoon_image', models.ImageField(blank=True, help_text="Cartoon version of client's image", null=True, upload_to='clients/cartoon/')),
                ('enabled', models.BooleanField(default=True, help_text='Enable or disable client review')),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
