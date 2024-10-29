# UserPage/urls.py
from django.urls import path
from .views import user_profile_view, User_login_view,user_logout_view,fetch_user_images,save_selected_images
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

app_name = 'UserPage'

urlpatterns = [
    # Uncomment the user profile path if needed
    path('UserPage/', user_profile_view, name='user_profile'),  
    path('Userlogin/', User_login_view, name="user_login"),  # Add a trailing slash
    path('logout/', user_logout_view, name='user_logout'),
    path('fetch-user-images/', fetch_user_images, name='fetch_user_images'),
    path('save-selected-images/', save_selected_images, name='save_selected_images'),
    path('Userlogin/', auth_views.LoginView.as_view(), name='user_login'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
