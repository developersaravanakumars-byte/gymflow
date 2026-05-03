from django.contrib import admin
from .models import Enquiry
@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'branch', 'source', 'status', 'created_at']
    list_filter = ['status', 'source', 'branch']
    search_fields = ['name', 'phone']
