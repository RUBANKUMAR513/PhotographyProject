# website/admin.py

from django.contrib import admin
from .models import CompanyInfo

class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = ('name','tagline', 'phone_number', 'email')

admin.site.register(CompanyInfo, CompanyInfoAdmin)
