# Generated by Django 5.1.2 on 2024-10-25 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserPage', '0004_image_product_delete_document'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='images',
            field=models.ManyToManyField(blank=True, related_name='products', to='UserPage.image'),
        ),
    ]
