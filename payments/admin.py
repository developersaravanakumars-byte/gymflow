from django.contrib import admin
from .models import Payment, Invoice
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['member', 'final_amount', 'status', 'method', 'coverage_from', 'coverage_to']
    list_filter = ['status', 'method', 'member__branch']
    search_fields = ['member__first_name', 'member__last_name']
@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'payment', 'issued_on']
