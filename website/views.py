from django.shortcuts import render
from .models import CompanyInfo
from .models import HomePageSlider
from .models import HomePageGallery
from .models import HappyClient
from django.http import JsonResponse
from .models import AboutUs
from django.db import models
from .models import BabyPropsGallery,BabyPropsImage
from .models import OurService,OurServicesImage
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models import Prefetch

def home_view(request):
    company_info = CompanyInfo.objects.first()
    sliders = HomePageSlider.objects.all()
    about_us_instance = AboutUs.objects.first()  # Only one instance should exist
    gallery_images = HomePageGallery.objects.filter(enable=True)
    happy_clients = HappyClient.objects.filter(enabled=True).order_by('-updated_at')[:10]
    # print(company_info)  # Check if the company info is being fetched
    # print(sliders)       # Check if sliders are being fetched
    
    context = {
        'company_info': company_info,
        'sliders': sliders,
        'gallery_images': gallery_images,
        'happy_clients': happy_clients,
        'about_us': about_us_instance
    }
    
    return render(request, 'home.html', context)


def index_view(request):
    company_info = CompanyInfo.objects.first()
    return render(request, 'index.html', {'company_info': company_info})

def baby_props_view(request):
    # Fetch the CompanyInfo instance (assuming only one instance exists)
    company_info = CompanyInfo.objects.first()

    # Fetch only enabled galleries and their enabled images
    galleries = BabyPropsGallery.objects.filter(enable=True).prefetch_related(
        models.Prefetch('images', queryset=BabyPropsImage.objects.filter(enable=True))
    )

    # Prepare context for the template
    context = {
        'company_info': company_info,
        'galleries': galleries
    }
    
    return render(request, 'BabyProps.html', context)


from django.utils.text import Truncator

def our_services_view(request):
    # Fetch the CompanyInfo instance (assuming only one instance exists)
    company_info = CompanyInfo.objects.first()
    
    if not company_info:
        return render(request, 'Services.html', {'error': 'Company information is missing.'})
    
    services = OurService.objects.filter(enable=True).prefetch_related(
        Prefetch('images', queryset=OurServicesImage.objects.filter(enable=True), to_attr='enabled_images')
    )
    
    # Split content by words, ensuring no new lines
    for service in services:
        word_limit = 15  # Number of words for main content
        words = service.content.split()
        service.main_content = " ".join(words[:word_limit])
        service.extra_content = " ".join(words[word_limit:]).strip()
    
    context = {
        'company_info': company_info,
        'services': services,
    }
    
    return render(request, 'Services.html', context)



def get_happy_clients(request):
    if request.method == 'POST':
        try:
            reviews = HappyClient.objects.filter(enabled=True)
            data = [
                {
                    'text': review.reviews,
                    'author': review.client_name,
                    'image': review.image.url,
                    'cartoon_image': review.cartoon_image.url
                } for review in reviews
            ]
            return JsonResponse(data, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)
    

def get_gif_duration(request):
    if request.method == 'POST':
        print("POST request received")  # Debug line
        try:
            company_info = CompanyInfo.objects.first()
            print("CompanyInfo:", company_info)  # Debug line
            
            if company_info:
                response_data = {}

                # Check for gif_duration
                if company_info.gif_duration:
                    response_data['gif_duration'] = company_info.gif_duration
                else:
                    response_data['gif_duration'] = None  # or any default value

                # Check for intro_gif (URL of the image)
                if company_info.intro_gif:
                    response_data['intro_gif_url'] = company_info.intro_gif.url
                else:
                    response_data['intro_gif_url'] = None  # or any default message like 'No GIF available'

                return JsonResponse(response_data)
            else:
                return JsonResponse({'error': 'Company info not found'}, status=404)

        except Exception as e:
            print("Error:", str(e))  # Debug line
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import OurService
import os
from django.conf import settings

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import OurService
from django.conf import settings
import os

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import OurService

@csrf_exempt
def get_service_images(request):
    if request.method == 'POST':
        try:
            print("Received POST request for service images")
            data = json.loads(request.body)
            service_id = data.get('service_id')

            if not service_id:
                return JsonResponse({'status': 'error', 'message': 'Service ID is required'}, status=400)

            service = OurService.objects.get(pk=service_id, enable=True)

            images = service.images.filter(enable=True).values_list('image', flat=True)
            print("Fetched images:", images)

            # Prepend MEDIA_URL to each image path
            image_paths = [f"{settings.MEDIA_URL}{image}" for image in images[1:]]
            print("All Image Paths (with MEDIA_URL):", image_paths)

            return JsonResponse({'status': 'success', 'images': image_paths})

        except OurService.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Service not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            print(f"Internal Server Error: {e}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)





