from django.contrib.auth import logout
from django.utils import timezone
from django.conf import settings
from django.utils import timezone
from django.conf import settings

class AutoLogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and request.user.is_staff:  # Check if the user is an admin
            last_activity_str = request.session.get('last_activity')

            # Convert the string back to a datetime object if it exists
            last_activity = timezone.datetime.fromisoformat(last_activity_str) if last_activity_str else None

            # Check if the user has been inactive for the specified session cookie age
            if last_activity:
                # Calculate the duration of inactivity
                if (timezone.now() - last_activity).total_seconds() > settings.SESSION_COOKIE_AGE:
                    logout(request)  # Log out the user
                else:
                    # Update the last activity timestamp as a string
                    request.session['last_activity'] = timezone.now().isoformat()  # Store as string
            else:
                # Set the last activity timestamp as a string if it doesn't exist
                request.session['last_activity'] = timezone.now().isoformat()  # Store as string

        response = self.get_response(request)
        return response


class TimeZoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Set the time zone to 'Asia/Kolkata' for all requests
        timezone.activate('Asia/Kolkata')

        response = self.get_response(request)
        return response

