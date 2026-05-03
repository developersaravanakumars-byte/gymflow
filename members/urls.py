from django.urls import path
from . import views
from .bulk_upload import bulk_upload

app_name = 'members'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('members/', views.member_list, name='list'),
    path('members/add/', views.member_create, name='create'),
    path('members/archived/', views.archived_list, name='archived'),
    path('members/bulk-upload/', bulk_upload, name='bulk_upload'),
    path('members/<int:pk>/', views.member_detail, name='detail'),
    path('members/<int:pk>/edit/', views.member_edit, name='edit'),
    path('members/<int:pk>/archive/', views.member_archive, name='archive'),
    path('members/<int:pk>/restore/', views.member_restore, name='restore'),
]
