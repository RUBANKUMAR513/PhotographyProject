# website/models.py

from django.db import models
from django.core.exceptions import ValidationError
from PIL import Image
import os
from io import BytesIO
from django.core.files.base import ContentFile

class CompanyInfo(models.Model):
    name = models.CharField(max_length=255)  # Required field
    intro_gif = models.ImageField(upload_to='company_intro_gifs/', blank=True, null=True)  # Optional GIF field
    gif_duration = models.FloatField(blank=True, null=True,help_text="In Seconds")   # Optional GIF duration field
    address_line1 = models.CharField(max_length=255,default="N/A")  # Required field
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    address_line3 = models.CharField(max_length=255, blank=True, null=True)
    address_line4 = models.CharField(max_length=255, blank=True, null=True)
    google_maps_link=models.URLField(blank=True, null=True)
    location_icon = models.ImageField(upload_to='icons/', default='default_location_icon.png', blank=True, null=True,help_text="Please Upload Animation GIF")
    phone_number = models.CharField(max_length=15)  # Required field
    phone_icon = models.ImageField(upload_to='icons/', default='default_phone_icon.png', blank=True, null=True,help_text="Please Upload Animation GIF")
    email = models.EmailField()  # Required field
    email_icon = models.ImageField(upload_to='icons/', default='default_email_icon.png', blank=True, null=True,help_text="Please Upload Animation GIF")
   
    # Tagline field with enable/disable option
    tagline = models.CharField(max_length=255, blank=True, null=True)
    enable_tagline = models.BooleanField(default=True)

    # Logos (required fields)
    footer_logo = models.ImageField(upload_to='logos/', default='default_logo.png')
    header_logo = models.ImageField(upload_to='logos/', default='default_logo.png')
    babyProps_header_logo=models.ImageField(upload_to='logos/', default='default_logo.png')
    sidebar_logo = models.ImageField(upload_to='logos/', default='default_logo.png')


    # Social media links with enable/disable checkboxes
    instagram_link = models.URLField(blank=True, null=True)
    enable_instagram = models.BooleanField(default=True)
    instagram_icon = models.ImageField(upload_to='icons/', default='default_instagram_icon.png', blank=True, null=True,help_text="Please Upload Animation GIF")

    youtube_link = models.URLField(blank=True, null=True)
    enable_youtube = models.BooleanField(default=True)
    youtube_icon = models.ImageField(upload_to='icons/', default='default_youtube_icon.png', blank=True, null=True,help_text="Please Upload Animation GIF")

    facebook_link = models.URLField(blank=True, null=True)
    enable_facebook = models.BooleanField(default=True)
    facebook_icon = models.ImageField(upload_to='icons/', default='default_facebook_icon.png', blank=True, null=True,help_text="Please Upload Animation GIF")

    x_link = models.URLField(blank=True, null=True, help_text="X was formerly known as Twitter")
    enable_x = models.BooleanField(default=True)
    x_video = models.FileField(upload_to='icons/', default='default_x_video.mp4', blank=True, null=True,help_text="Please Upload Animation Video")  # Changed to FileField

    whatsapp_link = models.URLField(blank=True, null=True)
    enable_whatsapp = models.BooleanField(default=True)
    whatsapp_icon = models.ImageField(upload_to='icons/', default='default_whatsapp_icon.png', blank=True, null=True,help_text="Please Upload Animation GIF")


    
    
   

    def __str__(self):
        return self.name


    def __str__(self):
        return self.name

    def clean(self):
        if CompanyInfo.objects.exists() and not self.pk:
            raise ValidationError("Only one instance of CompanyInfo can be created.")

    def save(self, *args, **kwargs):
        self.full_clean()  # This will call the clean method
        super(CompanyInfo, self).save(*args, **kwargs)


class HomePageSlider(models.Model):
    image = models.ImageField(upload_to='slider_images/')
    update_date_time = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        # Check for the maximum number of slider images
        if HomePageSlider.objects.count() >= 5 and not self.pk:  # Only for new instances
            raise ValidationError("You can only add a maximum of 5 slider images.")

        # Process the image for WebP format
        if self.image:
            # Open the image file
            img = Image.open(self.image)
            img_format = img.format  # Store the original format (e.g., 'JPEG', 'PNG')
            img = img.convert("RGB")  # Ensure compatibility with WebP format

            # Resize the image for background use (e.g., 1920x1080 for fullscreen backgrounds)
            target_size = (1920, 1080)
            img.thumbnail(target_size, Image.Resampling.LANCZOS)  # Use LANCZOS for high-quality resizing

            # Save the image in WebP format
            output = BytesIO()
            img.save(output, format='WEBP', quality=80)  # Adjust quality for performance
            output.seek(0)

            # Generate the WebP file name
            new_image_name = os.path.splitext(self.image.name)[0] + '.webp'

            # Replace the old image with the new WebP image
            self.image = ContentFile(output.read(), name=new_image_name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name





    

class HomePageGallery(models.Model):
    ORIENTATION_CHOICES = [
        ('portrait', 'Portrait'),
        ('landscape', 'Landscape'),
    ]

    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='gallery_images/')
    enable = models.BooleanField(default=True)  # Checkbox for enable/disable
    orientation = models.CharField(max_length=10, choices=ORIENTATION_CHOICES)
    update_date_time = models.DateTimeField(auto_now=True)  # Automatically set the date/time on update

    def clean(self):
        # Limit to 25 instances
        if HomePageGallery.objects.count() >= 25 and not self.pk:
            raise ValidationError('You can only create up to 25 Gallery Image Containers.')

    def save(self, *args, **kwargs):
        # Process the image for WebP format
        if self.image:
            # Open the image file
            img = Image.open(self.image)
            img = img.convert("RGB")  # Ensure compatibility with WebP format

            # Determine target size based on orientation
            if self.orientation == 'portrait':
                target_size = (1080, 1920)  # Example size for portrait
            else:
                target_size = (1920, 1080)  # Example size for landscape

            img.thumbnail(target_size, Image.Resampling.LANCZOS)  # Use LANCZOS for high-quality resizing

            # Save the image in WebP format
            output = BytesIO()
            img.save(output, format='WEBP', quality=80)  # Adjust quality for performance
            output.seek(0)

            # Replace the old image with the new WebP image
            new_image_name = os.path.splitext(self.image.name)[0] + '.webp'
            self.image = ContentFile(output.read(), name=new_image_name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class HappyClient(models.Model):
    reviews = models.TextField(max_length=1000, help_text="Client's review")
    client_name = models.CharField(max_length=255, help_text="Client's name")
    image = models.ImageField(upload_to='clients/', help_text="Client's image")
    cartoon_image = models.ImageField(upload_to='clients/cartoon/', help_text="Cartoon version of client's image", null=True, blank=True)
    enabled = models.BooleanField(default=True, help_text="Enable or disable client review")
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        # Limit to 10 instances
        if HappyClient.objects.count() >= 10 and not self.pk:
            raise ValidationError('You can only create up to 10 happy clients.')

    def save(self, *args, **kwargs):
        # Process the client's image
        if self.image:
            self.image = self.process_image(self.image, target_size=(1200, 3600))  # Resize to 12x36 inches (1200x3600 px)
        
        super().save(*args, **kwargs)

    @staticmethod
    def process_image(image_field, target_size):
        img = Image.open(image_field)
        img = img.convert("RGB")  # Ensure compatibility with WebP

        # Resize to the target size (12x36 inches)
        img.thumbnail(target_size, Image.Resampling.LANCZOS)

        # Compress and save the image to WebP format
        output = BytesIO()
        img.save(output, format="WEBP", quality=80)  # You can adjust the quality here
        output.seek(0)

        # Return a new ContentFile for the image field
        new_image_name = os.path.splitext(image_field.name)[0] + '.webp'
        return ContentFile(output.read(), name=new_image_name)

    def __str__(self):
        return self.client_name
    
class AboutUs(models.Model):
    content = models.TextField(max_length=968)  # Field to hold the content with a character limit of 968
    photographer_name = models.CharField(max_length=100, default="Photographername")
    photographer_image = models.ImageField(upload_to='photographers/', blank=True, null=True)  # Field for photographer's image
    updated_at = models.DateTimeField(auto_now=True)  # Automatically set to now when the object is updated

    class Meta:
        verbose_name = 'About Us'
        verbose_name_plural = 'About Us'

    def save(self, *args, **kwargs):
        # Ensure that only one instance of AboutUs can be created
        if not self.pk and AboutUs.objects.exists():
            raise ValidationError('Only one instance of About Us can be created.')

        # Process the photographer's image
        if self.photographer_image:
            self.photographer_image = self.process_image(self.photographer_image, target_size=(800, 800))  # Resize to 800x800

        super().save(*args, **kwargs)  # Call the original save method

    @staticmethod
    def process_image(image_field, target_size):
        img = Image.open(image_field)
        img = img.convert("RGB")  # Ensure compatibility with WebP
        img.thumbnail(target_size, Image.Resampling.LANCZOS)  # Resize

        # Save to WebP format
        output = BytesIO()
        img.save(output, format="WEBP", quality=80)
        output.seek(0)

        # Return a new ContentFile for the image field
        new_image_name = os.path.splitext(image_field.name)[0] + '.webp'
        return ContentFile(output.read(), name=new_image_name)

    def __str__(self):
        return 'About Us Content'

    
class BabyPropsGallery(models.Model):
    ORIENTATION_CHOICES = [
        ('portrait', 'Portrait'),
        ('landscape', 'Landscape'),
    ]
     
    name = models.CharField(max_length=255)
    enable = models.BooleanField(default=True)  # Checkbox for enable/disable
    update_date_time = models.DateTimeField(auto_now=True)  # Automatically set the date/time on update
    orientation = models.CharField(max_length=10, choices=ORIENTATION_CHOICES, default='portrait')

    def clean(self):
        # Limit to 25 instances
        if BabyPropsGallery.objects.count() >= 25 and not self.pk:
            raise ValidationError('You can only create up to 25 Baby Props Gallery.')

    def __str__(self):
        return self.name


class BabyPropsImage(models.Model):
    gallery = models.ForeignKey('BabyPropsGallery', related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='baby_props_images/')
    description = models.CharField(max_length=255, blank=True)  # Add description field
    enable = models.BooleanField(default=True)
    update_date_time = models.DateTimeField(auto_now=True)  # Automatically set the date/time on update

    @property
    def gallery_name(self):
        return self.gallery.name if self.gallery else "No Gallery"

    def save(self, *args, **kwargs):
        # Process the image before saving
        if self.image:
            self.image = self.process_image(self.image, target_size=(800, 800))  # Resize to 800x800
        super().save(*args, **kwargs)

    @staticmethod
    def process_image(image_field, target_size):
        img = Image.open(image_field)
        img = img.convert("RGB")  # Ensure compatibility with WebP
        img.thumbnail(target_size, Image.Resampling.LANCZOS)  # Resize

        # Save to WebP format
        output = BytesIO()
        img.save(output, format="WEBP", quality=80)
        output.seek(0)

        # Return a new ContentFile for the image field
        new_image_name = os.path.splitext(image_field.name)[0] + '.webp'
        return ContentFile(output.read(), name=new_image_name)

    def __str__(self):
        return f"Image for {self.gallery_name} - {self.description}"  # Updated string representation


class OurService(models.Model):
    ORIENTATION_CHOICES = [
        ('right', 'Right'),
        ('left', 'Left'),
    ]
    
    Service_name = models.CharField(max_length=255)
    enable = models.BooleanField(default=True)  # Checkbox for enable/disable
    content=models.TextField(blank=True, null=True)
    update_date_time = models.DateTimeField(auto_now=True)  # Automatically set the date/time on update
    orientation = models.CharField(max_length=10, choices=ORIENTATION_CHOICES, default='left',help_text="Align image Container")

    def clean(self):
        # Limit to 10 instances
        if OurService.objects.count() >= 10 and not self.pk:
            raise ValidationError('You can only create up to 10 Services.')

    def __str__(self):
        return self.Service_name


class OurServicesImage(models.Model):
    services = models.ForeignKey('OurService', related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='service_images/')
    description = models.CharField(max_length=255, blank=True)  # Optional description field
    enable = models.BooleanField(default=True)
    update_date_time = models.DateTimeField(auto_now=True)  # Automatically set the date/time on update

    @property
    def services_name(self):
        return self.services.Service_name if self.services else "No images"

    def save(self, *args, **kwargs):
        # Process the image before saving
        if self.image:
            self.image = self.process_image(self.image, target_size=(800, 800))  # Resize to 800x800
        super().save(*args, **kwargs)

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

    def __str__(self):
        return f"Image for {self.services_name} - {self.description}"  # Updated string representation
