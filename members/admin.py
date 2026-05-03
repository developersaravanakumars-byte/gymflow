from django.contrib import admin
from .models import Member

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'branch', 'phone', 'plan', 'membership_expiry', 'is_archived']
    list_filter = ['branch', 'is_archived', 'plan']
    search_fields = ['first_name', 'last_name', 'phone', 'email']
    date_hierarchy = 'joined_at'
