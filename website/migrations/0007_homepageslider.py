# Generated by Django 5.1.2 on 2024-10-22 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0006_remove_companyinfo_x_icon_companyinfo_x_video_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomePageSlider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='slider_images/')),
                ('update_date_time', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
    ]