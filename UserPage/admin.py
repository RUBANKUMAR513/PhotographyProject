from .models import UserDetail,UserImage,UserFavorite
from django.contrib import admin,messages
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import GroupAdmin
from django.urls import path,reverse
from django.utils.html import format_html
from django.shortcuts import render,redirect


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
        users = UserDetail.objects.all()  # Fetch UserDetails instances

        if request.method == 'POST':
            user_id = request.POST.get('user')
            images = request.FILES.getlist('images')

            # Fetch the UserDetails instance for the selected user
            user_details = UserDetail.objects.get(id=user_id)

            # Save each uploaded image to UserImages
            for image in images:
                UserImage.objects.create(user_details=user_details, photo=image)

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

class UserFavoritesAdmin(admin.ModelAdmin):
    list_display = ('user', 'photo_display', 'created_at')
    list_filter = (UserFilter,)  # Adds the user dropdown filter
    readonly_fields = ('user', 'image', 'created_at')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return True

    # Display thumbnail of the photo
    def photo_display(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return "No Image"

    photo_display.short_description = 'Photo Thumbnail'

# Register the model with the custom admin class
admin.site.register(UserFavorite, UserFavoritesAdmin)
