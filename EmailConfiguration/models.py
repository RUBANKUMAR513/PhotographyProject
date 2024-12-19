from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db.models.signals import post_migrate
from django.dispatch import receiver



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


@receiver(post_migrate)
def create_default_setting(sender, **kwargs):
    # Only create default if `Setting` model exists and has no entries
    if sender.name == 'EmailConfiguration':  # Replace 'your_app_name' with your app's name
        if not Setting.objects.exists():
            Setting.objects.create(
                host='smtp.gmail.com',
                port=587,
                email='rubanfebinosolutions@gmail.com',
                password='aijb eiho aoqo gvmf',
                status=True
            )

    

class ToEmail(models.Model):
    name = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    phonenumber = models.CharField(max_length=15, unique=True)
    position = models.CharField(max_length=100)
    active_status = models.BooleanField(default=False)
    send_otp = models.BooleanField(default=False)  # Checkbox for sending OTP
    send_ImgId = models.BooleanField(default=False)  # Checkbox for sending image ID

    def save(self, *args, **kwargs):
        # Ensure only the 'position' field is editable for the default instance
        if self.pk == 1:
            # Lock all fields except 'position'
           
            self.active_status = True  # Ensure active_status remains disabled

        # Limit the number of ToEmail instances to 5 only for new instances
        if not self.pk and ToEmail.objects.count() >= 5:
            raise ValidationError('You can only create up to 5 instances of ToEmail.')

        # Check for duplicate entries only if another instance has the same value
        duplicate_name = ToEmail.objects.filter(name=self.name).exclude(pk=self.pk).exists()
        duplicate_email = ToEmail.objects.filter(email=self.email).exclude(pk=self.pk).exists()
        duplicate_phonenumber = ToEmail.objects.filter(phonenumber=self.phonenumber).exclude(pk=self.pk).exists()

        if duplicate_name:
            raise ValidationError(f'A ToEmail entry with the name "{self.name}" already exists.')
        if duplicate_email:
            raise ValidationError(f'A ToEmail entry with the email "{self.email}" already exists.')
        if duplicate_phonenumber:
            raise ValidationError(f'A ToEmail entry with the phone number "{self.phonenumber}" already exists.')

        # If validation passes, proceed to save the instance
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Prevent deletion of the default instance
        if self.pk == 1:
            raise ValidationError("The default ToEmail instance cannot be deleted.")
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.name

# Signal to create default instance after migration
@receiver(post_migrate)
def create_default_toemail_instance(sender, **kwargs):
    if sender.name == 'EmailConfiguration':  # Replace 'your_app_name' with the actual app name
        if not ToEmail.objects.exists():
            ToEmail.objects.create(
                name="RUBAN KUMAR K",
                email="ceeeerubankumark513@gmail.com",
                phonenumber="6383817659",
                position="Developer",
                active_status=True
            )




class OTPModel(models.Model):
    email = models.EmailField(unique=True)  # Store the email address, ensure it's unique
    otp = models.CharField(max_length=4)  # Store the OTP (4-digit code)
    expires_at = models.DateTimeField()  # Store the expiration time of the OTP

    def is_expired(self):
        """Check if the OTP has expired."""
        return timezone.now() > self.expires_at

    def __str__(self):
        return f"OTP for {self.email} - {self.otp} (Expires at: {self.expires_at})"
