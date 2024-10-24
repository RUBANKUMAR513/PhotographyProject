# website/models.py

from django.db import models
from django.core.exceptions import ValidationError

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
        if HomePageSlider.objects.count() >= 5 and not self.pk:  # Only for new instances
            raise ValidationError("You can only add a maximum of 5 slider images.")
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
            raise ValidationError('You can only create up to 25 Gallery Image Container.')

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

    def __str__(self):
        return self.client_name
    
class AboutUs(models.Model):
    content = models.TextField(max_length=968)  # Field to hold the content with a character limit of 968
    photographer_name = models.CharField(max_length=100,default="Photographername")
    photographer_image = models.ImageField(upload_to='photographers/', blank=True, null=True)  # Field for photographer's image
    updated_at = models.DateTimeField(auto_now=True)  # Automatically set to now when the object is updated

    class Meta:
        verbose_name = 'About Us'
        verbose_name_plural = 'About Us'

    def save(self, *args, **kwargs):
        # Ensure that only one instance of AboutUs can be created
        if not self.pk and AboutUs.objects.exists():
            raise ValidationError('Only one instance of About Us can be created.')
        super().save(*args, **kwargs)  # Call the original save method

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
    gallery = models.ForeignKey(BabyPropsGallery, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='baby_props_images/')
    description = models.CharField(max_length=255, blank=True)  # Add description field
    update_date_time = models.DateTimeField(auto_now=True)  # Automatically set the date/time on update

    @property
    def gallery_name(self):
        return self.gallery.name if self.gallery else "No Gallery"

    def __str__(self):
        return f"Image for {self.gallery.name} - {self.description}"  # Update string representation