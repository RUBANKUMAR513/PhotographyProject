from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import os

class UserDetail(models.Model):
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
        super(UserDetail, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username}'s details"

# Signal to create UserDetails instance when a new User is created
@receiver(post_save, sender=User)
def create_user_details(sender, instance, created, **kwargs):
    if created:
        UserDetail.objects.create(user=instance)


class UserImage(models.Model):
    user_details = models.ForeignKey(
        UserDetail, on_delete=models.CASCADE, related_name="photos"
    )
    photo = models.ImageField(upload_to='show_photos/')
    
    def __str__(self):
        return f"{self.user_details.user.username}'s photo"
    def delete(self, *args, **kwargs):
        # Delete the photo file from the storage if it exists
        if self.photo:
            # This will delete the file from the server storage
            if os.path.isfile(self.photo.path):
                os.remove(self.photo.path)
        # Call the superclass's delete method to delete the database record
        super().delete(*args, **kwargs)



class UserFavorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    image = models.ForeignKey(UserImage, on_delete=models.CASCADE)
    src = models.CharField(max_length=500, blank=True, null=True)  # Add src field for image URL
    created_at = models.DateTimeField(auto_now_add=True)  # Optional: to track when the favorite was added

    def __str__(self):
        return f"{self.user.username}'s favorite image"

