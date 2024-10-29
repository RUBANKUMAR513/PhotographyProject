# UserPage/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from website.models import CompanyInfo
from django.contrib.auth import logout
from .models import UserImages,UserDetails
from django.http import JsonResponse
from django.core.paginator import Paginator

@login_required  # Ensures that only logged-in users can access this view
def user_profile_view(request):
    company_info = CompanyInfo.objects.first()
   
    # print(company_info)  # Check if the company info is being fetched
    # print(sliders)       # Check if sliders are being fetched
    
    context = {
        'company_info': company_info,
       
    }
    # You can pass additional context to the template if needed
    return render(request, 'UserPage.html',context)  # Ensure this matches your template name


def User_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_staff:
                messages.error(request, 'Admin users are not allowed to log in here.')
                return render(request, 'Userlogin.html')  # Render the login template again

            login(request, user)
            # messages.success(request, 'Login successful! Welcome to Vickyneo Photography.')
            return redirect('UserPage:user_profile')  # Redirect to the user profile page

        messages.error(request, 'Invalid username or password.')  # Add error message

    return render(request, 'Userlogin.html')  # Render the login template for GET requests


def user_logout_view(request):
    logout(request)  # Log out the user
    messages.success(request, 'You have been logged out successfully.')  # Optional success message
    return redirect('UserPage:user_login')  # Redirect to the login page


from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import UserImages, UserDetails

@login_required
def fetch_user_images(request):
    if request.method == 'POST':
        user_id = request.user.id
        user_images = UserImages.objects.filter(user_details__user_id=user_id).order_by('id')  # Order by ID or preferred field

        # Pagination
        page_number = int(request.POST.get('page', 1))
        paginator = Paginator(user_images, 8)  # 8 images per page
        page_obj = paginator.get_page(page_number)

        images_data = [
            {
                'id': img.id,
                'src': img.photo.url,  # URL for the image
                'alt': f"{img.user_details.user.username}'s photo"  # Alt text
            }
            for img in page_obj
        ]
        print(images_data)
        # Get user details (only allow_to_download)
        try:
            user_details = UserDetails.objects.get(user=request.user)
            allow_to_download = user_details.allow_to_download
        except UserDetails.DoesNotExist:
            allow_to_download = False  # Default value if user details do not exist

        return JsonResponse({
            'images': images_data,
            'total_pages': paginator.num_pages,  # Total number of pages
            'current_page': page_number,
            'allow_to_download': allow_to_download,
        })

    return JsonResponse({'images': [], 'allow_to_download': False})


