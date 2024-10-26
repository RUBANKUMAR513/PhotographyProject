from .models import UserDetails
from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import GroupAdmin

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







# admin.py
from django.contrib import admin
from .models import UserImages



@admin.register(UserImages)
class ShowPhotoAdmin(admin.ModelAdmin):
    list_display = ('user_details', 'photo')



# admin.py

# from django.contrib import admin
# from django.template.loader import get_template
# from django.utils.translation import gettext as _

# from .models import Show, ShowPhoto
# from .forms import ShowAdminForm


# class ShowPhotoInline(admin.TabularInline):
#     model = ShowPhoto
#     fields = ("showphoto_thumbnail",)
#     readonly_fields = ("showphoto_thumbnail",)
#     max_num = 0

#     def showphoto_thumbnail(self, instance):
        # """A (pseudo)field that returns an image thumbnail for a show photo."""
#         tpl = get_template("shows/admin/show_thumbnail.html")
#         return tpl.render({"photo": instance.photo})

#     showphoto_thumbnail.short_description =("Thumbnail")
