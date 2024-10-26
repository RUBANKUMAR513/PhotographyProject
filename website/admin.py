# website/admin.py

from django.contrib import admin
from .models import CompanyInfo
from .models import HomePageSlider
from .models import HomePageGallery
from .models import HappyClient
from .models import AboutUs
from .models import BabyPropsGallery, BabyPropsImage
from .forms import BabyPropsImageAdminForm
from .models import OurService,OurServicesImage
from .forms import OurServicesImageAdminForm

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

    # Override the has_add_permission method to disable the "Add" button
    def has_add_permission(self, request):
        # Disable add button if there are already 5 slider images
        if HomePageSlider.objects.count() >= 5:
            return False
        return True

admin.site.register(HomePageSlider, HomePageSliderAdmin)

class HomePageGalleryAdmin(admin.ModelAdmin):
    list_display = ('name', 'enable', 'orientation', 'update_date_time')
    list_filter = ('enable', 'orientation')
    search_fields = ('name',)

    # Override the has_add_permission method to disable the "Add" button
    def has_add_permission(self, request):
        # Disable add button if there are already 25 slider images
        if HomePageGallery.objects.count() >= 25:
            return False
        return True

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
    # Override the has_add_permission method to disable the "Add" button
    def has_add_permission(self, request):
        # Disable add button if there are already 10 slider images
        if HappyClient.objects.count() >= 10:
            return False
        return True

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



    
class BabyPropsImageAdmin(admin.ModelAdmin):
    form = BabyPropsImageAdminForm
    list_display = ('gallery_name', 'description','enable', 'update_date_time')  # Include description
    fields = ('gallery', 'image', 'description','enable','update_date_time')  # Fields to be shown in the edit form
    readonly_fields = ('update_date_time',)  # Make update_date_time read-only if you don't want it editable



class BabyPropsGalleryAdmin(admin.ModelAdmin):
    list_display = ('name', 'enable','update_date_time')
    fields =('name','orientation','enable','update_date_time')
    readonly_fields = ('update_date_time',)

     # Override the has_add_permission method to disable the "Add" button
    def has_add_permission(self, request):
        # Disable add button if there are already 25 baby props galleries
        if BabyPropsGallery.objects.count() >= 25:
            return False
        return True

# Register models with the admin site
admin.site.register(BabyPropsImage, BabyPropsImageAdmin)
admin.site.register(BabyPropsGallery, BabyPropsGalleryAdmin)


class OurServicesImageAdmin(admin.ModelAdmin):
    form = OurServicesImageAdminForm
    list_display = ('services_name', 'description', 'enable', 'update_date_time')  # Include description
    fields = ('services', 'image','description', 'enable', 'update_date_time')  # Fields to be shown in the edit form
    readonly_fields = ('update_date_time',)  # Make update_date_time read-only if you don't want it editable


class OurServicesAdmin(admin.ModelAdmin):
    list_display = ('Service_name', 'enable', 'update_date_time')
    fields = ('Service_name', 'content', 'orientation', 'enable', 'update_date_time')
    readonly_fields = ('update_date_time',)

    # Override the has_add_permission method to disable the "Add" button
    def has_add_permission(self, request):
        # Disable add button if there are already 10 Services
        if OurService.objects.count() >= 10:
            return False
        return True


# Register models with the admin site
admin.site.register(OurService, OurServicesAdmin)
admin.site.register(OurServicesImage, OurServicesImageAdmin)





   

