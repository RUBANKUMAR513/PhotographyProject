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
from .tasks import send_email_task


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
        print("user_id",user_id)
        user_images = UserImage.objects.filter(user_details__user_id=user_id).order_by('id')
        print("user_images",user_images)
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



@login_required
@csrf_exempt
def update_favorite_image(request, action):
    data = json.loads(request.body)
    image_id = data.get('image_id')

    # Get the image object based on image_id
    image_obj = UserImage.objects.get(id=image_id)
    print("user",request.user)
    if action == 'add':
        # Get or create a UserFavorite and also store the image URL in the `src` field
        favorite, created = UserFavorite.objects.get_or_create(
            user=request.user,
            image=image_obj,
            defaults={'src': image_obj.photo.url}  # Set the src field to the image URL
        )
        if not created:
            # If the favorite already exists, you can update the src field (optional)
            favorite.src = image_obj.photo.url
            favorite.save()

    elif action == 'remove':
        UserFavorite.objects.filter(user=request.user, image=image_obj).delete()

    return JsonResponse({'status': 'success'})

@login_required
def get_favorites(request):
    # Fetch favorites for the current user, using select_related to optimize the query
    favorites = UserFavorite.objects.filter(user=request.user).select_related('image')

    # Extract the 'photo' field and 'src' field from the related UserImage model
    favorite_images = favorites.values('image__id','image__photo', 'src')  # Using the double underscore to access the related field

    return JsonResponse({'favorites': list(favorite_images)})


@csrf_exempt
def save_selected_images(request):
    if request.method == 'POST':
        try:
            # Parse incoming request data
            data = json.loads(request.body)
            image_ids = data.get('imageIds', [])
            print(f"Received image IDs: {image_ids}")

            if not image_ids:
                print("No image IDs provided")
                return JsonResponse({'error': 'No image IDs provided'}, status=400)

            images = UserFavorite.objects.filter(image__id__in=image_ids)

            if not images.exists():
                print(f"No images found for IDs: {image_ids}")
                return JsonResponse({'error': 'Some image IDs are invalid'}, status=400)

            user = request.user
            user.favorites.set(images)
            print(f"Successfully saved {len(images)} images for user {user.username}")

            # Send the response immediately
            response = JsonResponse({'success': True, 'message': 'Images saved successfully'})

            # Process send_url_to_mail asynchronously with Celery
            send_email_task.delay(image_ids, user.id)

            return response

        except Exception as e:
            print(f"Error occurred while saving images: {e}")  # Print the error
            return JsonResponse({'error': str(e)}, status=500)

    print("Invalid request method: Expected POST.")
    return JsonResponse({'error': 'Invalid request method'}, status=405)