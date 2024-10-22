# website/models.py

from django.db import models
from django.core.exceptions import ValidationError

class CompanyInfo(models.Model):
    name = models.CharField(max_length=255)  # Required field
    address_line1 = models.CharField(max_length=255,default="N/A")  # Required field
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    address_line3 = models.CharField(max_length=255, blank=True, null=True)
    address_line4 = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=15)  # Required field
    email = models.EmailField()  # Required field

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

    youtube_link = models.URLField(blank=True, null=True)
    enable_youtube = models.BooleanField(default=True)

    facebook_link = models.URLField(blank=True, null=True)
    enable_facebook = models.BooleanField(default=True)

    x_link = models.URLField(blank=True, null=True, help_text="X was formerly known as Twitter")
    enable_x = models.BooleanField(default=True)

    whatsapp_link = models.URLField(blank=True, null=True)
    enable_whatsapp = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def clean(self):
        if CompanyInfo.objects.exists() and not self.pk:
            raise ValidationError("Only one instance of CompanyInfo can be created.")

    def save(self, *args, **kwargs):
        self.full_clean()  # This will call the clean method
        super(CompanyInfo, self).save(*args, **kwargs)

