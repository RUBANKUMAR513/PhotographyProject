from django.urls import path
from .views import home_view, index_view,baby_props_view,Our_services_view,get_happy_clients,get_gif_duration
from django.conf import settings
from django.conf.urls.static import static

app_name = 'website'

urlpatterns = [
    path('', index_view, name='index'),  # Assuming the index page is the homepage
    path('home/', home_view, name='home'),
    path('babyProps/',baby_props_view,name='babyprops'),
    path('ourServices/',Our_services_view,name='services'),
    path('get-happy-clients/', get_happy_clients, name='get_reviews'),  # Replace with your endpoint URL
    path('get-gif-duration/', get_gif_duration, name='get_gif_duration'),
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)