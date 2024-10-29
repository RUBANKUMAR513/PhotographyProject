# UserPage/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from website.models import CompanyInfo
from django.contrib.auth import logout
from .models import UserImage,UserDetail,UserFavorite
from django.http import JsonResponse
from django.core.paginator import Paginator
import json

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





@login_required
def fetch_user_images(request):
    if request.method == 'POST':
        try:
            # Parse JSON data from request body
            data = json.loads(request.body)
            page_number = int(data.get('page', 1))  # Defaults to 1 if not provided
            print('Requested page number:', page_number)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        user_id = request.user.id
        user_images = UserImage.objects.filter(user_details__user_id=user_id).order_by('id')
        
        paginator = Paginator(user_images, 8)  # 8 images per page
        page_obj = paginator.get_page(page_number)

        images_data = [
            {
                'id': img.id,
                'src': img.photo.url,
                'alt': f"{img.user_details.user.username}'s photo"
            }
            for img in page_obj
        ]

        try:
            user_details = UserDetail.objects.get(user=request.user)
            allow_to_download = user_details.allow_to_download
        except UserDetail.DoesNotExist:
            allow_to_download = False

        return JsonResponse({
            'images': images_data,
            'total_pages': paginator.num_pages,
            'current_page': page_number,
            'allow_to_download': allow_to_download,
        })

    return JsonResponse({'images': [], 'allow_to_download': False})






@csrf_exempt  # Use this if you're not using CSRF protection in development; remove in production
def save_selected_images(request):
    if request.method == 'POST':
        try:
            # Load the JSON data from the request body
            data = json.loads(request.body)
            selected_image_ids = data.get('imageIds', [])  # Expecting 'imageIds'

            # Ensure the user is authenticated before proceeding
            # You might need to adjust this part based on your authentication setup
            user = request.user  
            if not user.is_authenticated:
                return JsonResponse({'status': 'error', 'message': 'User is not authenticated.'}, status=403)

            # Delete all existing favorites for the user
            UserFavorite.objects.filter(user=user).delete()

            # Process the selected images
            for image_id in selected_image_ids:
                try:
                    # Fetch the image from UserImages model using the image_id
                    user_image = UserImage.objects.get(id=image_id)

                    # Save the image as a new favorite for the user
                    UserFavorite.objects.create(user=user, image=user_image.photo)

                except UserImage.DoesNotExist:
                    return JsonResponse({'status': 'error', 'message': f'Image with ID {image_id} does not exist.'}, status=404)

            return JsonResponse({'status': 'success', 'message': 'Images saved successfully!'}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data.'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)
