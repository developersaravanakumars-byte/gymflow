from django.urls import path
from . import views
app_name = 'payments'
urlpatterns = [
    path('', views.payment_list, name='list'),
    path('add/', views.payment_create, name='create'),
    path('<int:pk>/', views.payment_detail, name='detail'),
    path('pending/', views.pending_payments, name='pending'),
    path('invoice/<int:pk>/pdf/', views.invoice_pdf, name='invoice_pdf'),
]
