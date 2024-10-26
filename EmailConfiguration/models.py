from django.db import models
from django.utils import timezone

# Create your models here.
from django.core.exceptions import ValidationError

class Setting(models.Model):
    host = models.CharField(max_length=255)
    port = models.IntegerField()
    email = models.EmailField()
    password = models.CharField(max_length=255)
    status = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.pk and Setting.objects.exists():
            raise ValidationError('There can be only one instance of Settings.')
        super(Setting, self).save(*args, **kwargs)

    def __str__(self):
        return self.email
    
class ToEmail(models.Model):
    name = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    phonenumber = models.CharField(max_length=15, unique=True)
    position = models.CharField(max_length=100)
    active_status = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Limit the number of ToEmail instances to 5
        if not self.pk and ToEmail.objects.count() >= 5:
            raise ValidationError('You can only create up to 5 instances of ToEmail.')

        # Check for duplicate entries
        if ToEmail.objects.filter(name=self.name).exclude(pk=self.pk).exists():
            raise ValidationError(f'A ToEmail entry with the name "{self.name}" already exists.')
        if ToEmail.objects.filter(email=self.email).exclude(pk=self.pk).exists():
            raise ValidationError(f'A ToEmail entry with the email "{self.email}" already exists.')
        if ToEmail.objects.filter(phonenumber=self.phonenumber).exclude(pk=self.pk).exists():
            raise ValidationError(f'A ToEmail entry with the phone number "{self.phonenumber}" already exists.')

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    


class OTPModel(models.Model):
    email = models.EmailField(unique=True)  # Store the email address, ensure it's unique
    otp = models.CharField(max_length=4)  # Store the OTP (4-digit code)
    expires_at = models.DateTimeField()  # Store the expiration time of the OTP

    def is_expired(self):
        """Check if the OTP has expired."""
        return timezone.now() > self.expires_at

    def __str__(self):
        return f"OTP for {self.email} - {self.otp} (Expires at: {self.expires_at})"
