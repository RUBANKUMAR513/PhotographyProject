from celery import shared_task
from .models import UserFavorite,User
from EmailConfiguration.msg import send_url_to_mail
from .models import UserImage, UserDetail

@shared_task
def send_email_task(image_ids, user_id):
    try:
        # Retrieve the images and user from the database
        images = UserFavorite.objects.filter(image__id__in=image_ids)
        user = User.objects.get(id=user_id)
        
        # Call the send_url_to_mail function
        send_url_to_mail(images, user)
        print(f"Email sent successfully for user {user.username}")
    except Exception as e:
        print(f"Error occurred while sending email: {e}")


from django.core.files.uploadedfile import SimpleUploadedFile
from UserPage.models import UserImage, UserDetail
from django.contrib import messages
from django.shortcuts import render, redirect
from celery import shared_task
import logging
import os
from django.core.files import File

logger = logging.getLogger(__name__)


@shared_task
def save_images(image_paths, user_id):
    user_details = UserDetail.objects.get(id=user_id)
    batch_size = 500

    for i in range(0, len(image_paths), batch_size):
        batch = image_paths[i:i + batch_size]
        for path in batch:
            with open(path, 'rb') as image_file:
                django_file = File(image_file)
                filename = os.path.basename(path)
                UserImage.objects.create(user_details=user_details, photo=django_file)
            os.remove(path)
