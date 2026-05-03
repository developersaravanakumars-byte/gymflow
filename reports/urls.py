from django.urls import path
from . import views
app_name = 'reports'
urlpatterns = [
    path('', views.report_home, name='home'),
    path('revenue/', views.revenue_report, name='revenue'),
    path('expiry/', views.expiry_report, name='expiry'),
    path('pending/', views.pending_report, name='pending'),
    path('members/export/', views.export_members_excel, name='export_members'),
]
