from django.urls import path
from . import views
app_name = 'enquiries'
urlpatterns = [
    path('', views.enquiry_list, name='list'),
    path('add/', views.enquiry_create, name='create'),
    path('<int:pk>/', views.enquiry_detail, name='detail'),
    path('<int:pk>/edit/', views.enquiry_edit, name='edit'),
    path('<int:pk>/convert/', views.enquiry_convert, name='convert'),
]
