# UserPage/urls.py
from django.urls import path
from .views import user_profile_view, User_login_view,user_logout_view
from django.conf import settings
from django.conf.urls.static import static
from .admin import UserDetailsAdmin

app_name = 'UserPage'

urlpatterns = [
    # Uncomment the user profile path if needed
    path('UserPage/', user_profile_view, name='user_profile'),  
    path('Userlogin/', User_login_view, name="user_login"),  # Add a trailing slash
    path('logout/', user_logout_view, name='user_logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
