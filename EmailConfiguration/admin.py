from django.contrib import admin
from django.core.exceptions import ValidationError
from django import forms
from .models import Setting, ToEmail
from .forms import SettingForm, ToEmailForm


class SettingAdmin(admin.ModelAdmin):
    form = SettingForm  # Use the custom form for validation
    list_display = ('host', 'port', 'email', 'status')

    def has_add_permission(self, request):
        # Limit to only one instance of Setting
        if Setting.objects.exists():
            return False
        return True

    def save_model(self, request, obj, form, change):
        if not change and Setting.objects.exists():
            raise ValidationError('Only one instance of Setting is allowed. Please edit the existing instance.')
        super().save_model(request, obj, form, change)


class ToEmailAdmin(admin.ModelAdmin):
    form = ToEmailForm  # Use the custom form for validation
    list_display = ('name', 'email', 'phonenumber', 'position', 'active_status')
    list_filter = ('active_status', 'position')

    def has_add_permission(self, request):
        # Limit ToEmail instances to 5
        if ToEmail.objects.count() >= 5:
            return False
        return True

    def save_model(self, request, obj, form, change):
        # Prevent saving if adding a new instance would exceed 5 instances
        if not change and ToEmail.objects.count() >= 5:
            raise ValidationError('You can only create up to 5 instances of ToEmail.')
        super().save_model(request, obj, form, change)

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.pk == 1:  # If editing the default instance
            return ['active_status']  # Make only active_status read-only
        return self.readonly_fields  # For all other instances, use default readonly fields
    
    def has_delete_permission(self, request, obj=None):
        if obj and obj.pk == 1:  # Prevent deletion of the default instance
            return False
        return super().has_delete_permission(request, obj)


# Register the models with their respective admin classes
admin.site.register(Setting, SettingAdmin)
admin.site.register(ToEmail, ToEmailAdmin)
