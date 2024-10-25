from django.db import models
from django.utils import timezone
from datetime import timedelta

class UserDetails(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    date_of_shoots = models.DateField()
    description = models.TextField(blank=True, null=True)
    allow_to_download = models.BooleanField(default=False)
    remove_on = models.DateTimeField()
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

