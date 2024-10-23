from django.shortcuts import render
from .models import CompanyInfo
from .models import HomePageSlider
from .models import HomePageGallery
from .models import HappyClient
from django.http import JsonResponse
from .models import AboutUs

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
    return render(request, 'index.html')

def baby_props_view(request):
     # Fetch the CompanyInfo instance (assuming only one instance exists)
    company_info = CompanyInfo.objects.first()  # Get the first (and only) instance
    
    context = {
        'company_info': company_info
    }
    return render(request,'BabyProps.html', context)

def Our_services_view(request):
     # Fetch the CompanyInfo instance (assuming only one instance exists)
    company_info = CompanyInfo.objects.first()  # Get the first (and only) instance
    
    context = {
        'company_info': company_info
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