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
    company_info = CompanyInfo.objects.first()
    return render(request, 'index.html', {'company_info': company_info})

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
    

def get_gif_duration(request):
    if request.method == 'POST':
        print("POST request received")  # Debug line
        try:
            company_info = CompanyInfo.objects.first()
            print("CompanyInfo:", company_info)  # Debug line
            if company_info and company_info.gif_duration:
                return JsonResponse({'gif_duration': company_info.gif_duration})
            else:
                return JsonResponse({'error': 'GIF duration not found'}, status=404)
        except Exception as e:
            print("Error:", str(e))  # Debug line
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=400)


# In your_app/views.py

from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login

class CustomAdminLoginView(LoginView):
    template_name = 'admin/login.html'
    form_class = AuthenticationForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request, data=request.POST)
        otp = request.POST.get('otp')

        if form.is_valid():
            user = form.get_user()

            # Check if OTP is provided
            if not otp:
                messages.error(request, 'OTP is required.')
            else:
                # OTP validation logic (replace with real OTP logic)
                if otp == "1234":  # Example OTP for demonstration
                    login(request, user)
                    return redirect('admin:index')
                else:
                    messages.error(request, 'Invalid OTP.')
        else:
            messages.error(request, 'Invalid username or password.')

        # Render the login form with error messages on failure
        return render(request, self.template_name, {'form': form})



