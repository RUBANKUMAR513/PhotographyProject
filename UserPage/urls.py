from django.urls import path
from .views import user_profile_view,User_login_view
from django.conf import settings
from django.conf.urls.static import static

app_name = 'UserPage'

urlpatterns = [
    # path('', user_profile_view, name='user_profile'),  
    path('Userlogin',User_login_view,name="user_login"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)