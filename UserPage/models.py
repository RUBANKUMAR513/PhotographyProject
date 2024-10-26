from django.db import models
from django.utils import timezone
from datetime import timedelta

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

class UserDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_shoots = models.DateField(default=timezone.now)
    description = models.TextField(blank=True, null=True)
    allow_to_download = models.BooleanField(default=False)
    remove_on = models.DateTimeField(default=timezone.now)
    remaining_days = models.IntegerField(editable=False)
    last_updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Calculate remaining days based on remove_on field
        if self.remove_on:
            self.remaining_days = (self.remove_on.date() - timezone.now().date()).days
        else:
            self.remaining_days = None
        super(UserDetails, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username}'s details"

# Signal to create UserDetails instance when a new User is created
@receiver(post_save, sender=User)
def create_user_details(sender, instance, created, **kwargs):
    if created:
        UserDetails.objects.create(user=instance)


class UserImages(models.Model):
    user_details = models.ForeignKey(
        UserDetails, on_delete=models.CASCADE, related_name="photos"
    )
    photo = models.ImageField(upload_to='show_photos/')
    
    def __str__(self):
        return f"{self.user_details.user.username}'s photo"




