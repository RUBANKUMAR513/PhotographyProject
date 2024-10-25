from django.contrib import admin
from django.contrib import admin
from .models import UserDetails

@admin.register(UserDetails)
class UserDetailsAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = (
        'user', 'date_of_shoots', 'description', 
        'allow_to_download', 'remove_on', 'remaining_days', 'last_updated'
    )
    # Fields to filter in the sidebar
    list_filter = ('allow_to_download', 'date_of_shoots', 'remove_on')
    # Fields to search in the search bar
    search_fields = ('user__username', 'description')
    # Fields that are read-only in the admin interface
    readonly_fields = ('remaining_days', 'last_updated')

    # Customizing the form display in the detail view
    fieldsets = (
        (None, {
            'fields': ('user', 'date_of_shoots', 'description')
        }),
        ('Permissions', {
            'fields': ('allow_to_download',)
        }),
        ('Removal and Tracking', {
            'fields': ('remove_on', 'remaining_days', 'last_updated')
        }),
    )

    # Automatically calculates the remaining days upon saving the form in the admin
    def save_model(self, request, obj, form, change):
        obj.save()  # Remaining days calculation is handled in the model's `save` method

