# website/admin.py

from django.contrib import admin
from .models import CompanyInfo
from .models import HomePageSlider
from .models import HomePageGallery
from .models import HappyClient
from .models import AboutUs


class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = ('name','tagline', 'phone_number', 'email')

    def has_add_permission(self, request):
        # Disable the add button in the admin
        return not AboutUs.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Optionally disable the delete button
        return False

admin.site.register(CompanyInfo, CompanyInfoAdmin)



class HomePageSliderAdmin(admin.ModelAdmin):
    list_display = ('name', 'update_date_time')

admin.site.register(HomePageSlider,HomePageSliderAdmin )

class HomePageGalleryAdmin(admin.ModelAdmin):
    list_display = ('name', 'enable', 'orientation', 'update_date_time')
    list_filter = ('enable', 'orientation')
    search_fields = ('name',)

admin.site.register(HomePageGallery,HomePageGalleryAdmin )

class HappyClientAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'enabled', 'updated_at')  # Displays these fields in the list view
    list_filter = ('enabled', 'updated_at')  # Adds filter options in the admin
    search_fields = ('client_name', 'reviews')  # Adds search functionality by client name and reviews
    readonly_fields = ('updated_at',)  # Makes 'updated_at' read-only in the form
    fieldsets = (
        (None, {
            'fields': ('client_name', 'reviews', 'image', 'cartoon_image', 'enabled')
        }),
        ('Timestamps', {
            'fields': ('updated_at',)
        }),
    )

admin.site.register(HappyClient, HappyClientAdmin)


class AboutUsAdmin(admin.ModelAdmin):
    list_display = ('id', 'content_preview', 'updated_at')  # Display these fields in the list view
    readonly_fields = ('updated_at',)  # Make the updated_at field read-only in the admin
    
    def content_preview(self, obj):
        # This method provides a preview of the content
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content Preview'  # Column title in admin

    def has_add_permission(self, request):
        # Disable the add button in the admin
        return not AboutUs.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Optionally disable the delete button
        return False

admin.site.register(AboutUs, AboutUsAdmin)