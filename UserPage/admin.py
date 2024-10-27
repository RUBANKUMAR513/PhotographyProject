from .models import UserDetails,UserImages
from django.contrib import admin,messages
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import GroupAdmin
from django.urls import path,reverse
from django.utils.html import format_html
from django.shortcuts import render,redirect


@admin.register(UserDetails)
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
            f'/admin/{self.model._meta.app_label}/userdetails/upload_images/'
        )
    link_to_upload_images.short_description = 'Upload Images'

    # Override get_urls to add a custom upload images page URL
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('upload_images/', self.admin_site.admin_view(self.upload_images_view), name='upload_images'),
        ]
        return custom_urls + urls

    # Define the upload images view
    def upload_images_view(self, request):
        users = UserDetails.objects.all()  # Fetch UserDetails instances

        if request.method == 'POST':
            user_id = request.POST.get('user')
            images = request.FILES.getlist('images')

            # Fetch the UserDetails instance for the selected user
            user_details = UserDetails.objects.get(id=user_id)

            # Save each uploaded image to UserImages
            for image in images:
                UserImages.objects.create(user_details=user_details, photo=image)

            # Set a success message
            messages.success(request, "Images successfully uploaded.")

            # Redirect to the UserDetails list view
            return redirect('/admin/UserPage/userdetails/')

        # Render the upload form with user dropdown
        return render(request, 'UploadImages.html', {'users': users})





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




@admin.register(UserImages)
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














