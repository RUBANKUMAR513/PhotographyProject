from celery import shared_task
from .models import UserFavorite,User
from EmailConfiguration.msg import send_url_to_mail

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
