from django.core.management.base import BaseCommand
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from website.models import (
    HomePageSlider, HomePageGallery, HappyClient,
    BabyPropsImage, OurServicesImage, AboutUs
)
import os

class Command(BaseCommand):
    help = 'Update existing images to WebP format and resize them'

    def handle(self, *args, **kwargs):
        models_to_update = [
            HomePageSlider, HomePageGallery, HappyClient,
            BabyPropsImage, OurServicesImage, AboutUs  # Added AboutUs here
        ]
        target_size = (800, 800)  # Adjust as needed

        for model in models_to_update:
            self.stdout.write(f"Processing {model.__name__}...")
            records = model.objects.all()
            updated_count = 0

            for record in records:
                if hasattr(record, 'image') and record.image:
                    old_image = record.image
                    record.image = self.process_image(record.image, target_size)
                    record.save()
                    updated_count += 1
                    self.stdout.write(f"Updated image for record ID {record.id}")
                    
                    # Optionally delete old image to save storage
                    if old_image.name != record.image.name:
                        old_image.delete(save=False)

                # Handle photographer_image field for AboutUs model
                if isinstance(record, AboutUs) and hasattr(record, 'photographer_image') and record.photographer_image:
                    old_image = record.photographer_image
                    record.photographer_image = self.process_image(record.photographer_image, target_size)
                    record.save()
                    updated_count += 1
                    self.stdout.write(f"Updated photographer image for AboutUs record ID {record.id}")

                    # Optionally delete old image to save storage
                    if old_image.name != record.photographer_image.name:
                        old_image.delete(save=False)

            self.stdout.write(f"Updated {updated_count} images for {model.__name__}")

    @staticmethod
    def process_image(image_field, target_size):
        img = Image.open(image_field)
        img = img.convert("RGB")  # Ensure compatibility with WebP format
        img.thumbnail(target_size, Image.Resampling.LANCZOS)  # Resize the image

        # Save the image in WebP format
        output = BytesIO()
        img.save(output, format="WEBP", quality=80)  # Adjust quality if needed
        output.seek(0)

        # Return a new ContentFile to update the image field
        new_image_name = os.path.splitext(image_field.name)[0] + '.webp'
        return ContentFile(output.read(), name=new_image_name)
