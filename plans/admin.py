from django.contrib import admin
from .models import Plan
@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'duration', 'duration_unit', 'price', 'is_active']
    list_filter = ['is_active', 'duration_unit']
