from .models import UserDetail,UserImage,UserFavorite
from django.contrib import admin,messages
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import GroupAdmin
from django.urls import path,reverse
from django.utils.html import format_html
from django.shortcuts import render,redirect
from .tasks import save_images
import logging
import os
import uuid

logger = logging.getLogger(__name__)


@admin.register(UserDetail)
class UserDetailsAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = (
        'user', 'date_of_shoots', 'description', 
        'allow_to_download', 'remove_on', 'remaining_days', 
        'last_updated', 'link_to_upload_images'
    )

    # Custom link for uploading images in list display
    def link_to_upload_images(self, obj):
        return format_html(
            '<a href="{}">Upload Images</a>',
            f'/admin/{self.model._meta.app_label}/{self.model._meta.model_name}/upload_images/'
        )
    link_to_upload_images.short_description = 'Upload Images'

    # Override get_urls to add a custom upload images page URL
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('upload_images/', self.admin_site.admin_view(self.upload_images_view), name='upload_images'),
        ]
        return custom_urls + urls

    def upload_images_view(self,request):
        """
        Function-based view to handle uploading images for a user.
        """
        if request.method == 'GET':
            # Fetch all users for the dropdown in the form
            users = UserDetail.objects.all()
            return render(request, 'UploadImages.html', {'users': users})

        elif request.method == 'POST':
            # Get user ID and uploaded images
            user_id = request.POST.get('user')
            images = request.FILES.getlist('images')

            # Validate the input
            if not user_id:
                messages.error(request, "User selection is required.")
                return redirect(request.path)
            if not images:
                messages.error(request, "Please upload at least one image.")
                return redirect(request.path)

            # Convert images to a list of file paths
            temp_storage_path = 'temporary_storage/'
            if not os.path.exists(temp_storage_path):
                os.makedirs(temp_storage_path)
            # print("still in their fuctions")
            image_paths = []
            for image in images:
                # Save images temporarily with a unique filename
                unique_filename = f"{uuid.uuid4()}_{image.name}"
                path = os.path.join(temp_storage_path, unique_filename)
                with open(path, 'wb+') as destination:
                    for chunk in image.chunks():
                        destination.write(chunk)
                image_paths.append(path)

            print("outer the loop")
            # Call Celery task to process images
            save_images.delay(image_paths, user_id)

            # Immediate success message
            messages.success(request, "Images are being uploaded. You will be notified once completed.")
            # Redirect to admin page for `UserImage` model
            admin_url = reverse(f'admin:{UserImage._meta.app_label}_{UserImage._meta.model_name}_changelist')
            return redirect(admin_url)







# Inline model to display users in the Group admin
class UserInline(admin.TabularInline):
    model = User.groups.through  # Allows access to the Group-User relationship
    extra = 1  # Number of extra blank user rows to display

# Custom Group admin to include User inline
class CustomGroupAdmin(GroupAdmin):
    inlines = [UserInline]

# Unregister the default Group admin
admin.site.unregister(Group)

# Register Group with the customized admin
admin.site.register(Group, CustomGroupAdmin)




@admin.register(UserImage)
class UserImagesAdmin(admin.ModelAdmin):
    # Display fields in the list view
    list_display = ('user_details', 'photo_display')
    
    # Add a filter by user details
    list_filter = ('user_details',)

    # Display thumbnail of the photo (optional)
    def photo_display(self, obj):
        return format_html('<img src="{}" width="50" height="50" />', obj.photo.url)
    photo_display.short_description = 'Photo Thumbnail'

    # Optional: Adjust the display for the ForeignKey field to show the user's name
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('user_details__user')  # Optimize with select_related
        return queryset

    def user_name(self, obj):
        return obj.user_details.user.username
    user_name.short_description = 'User Name'













# Custom filter to list all users
class UserFilter(admin.SimpleListFilter):
    title = 'User'  # Display name for the filter
    parameter_name = 'user'  # Query parameter name

    def lookups(self, request, model_admin):
        # Returns a list of tuples with user IDs and usernames for the dropdown
        return [(user.id, user.username) for user in User.objects.all()]

    def queryset(self, request, queryset):
        # Filters the queryset based on the selected user
        if self.value():
            return queryset.filter(user_id=self.value())
        return queryset

class UserFavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'image', 'src', 'created_at')  # Include 'src' field in the admin list view

admin.site.register(UserFavorite, UserFavoriteAdmin)


