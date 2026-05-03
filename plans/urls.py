from django.urls import path
from . import views
app_name = 'plans'
urlpatterns = [
    path('', views.plan_list, name='list'),
    path('add/', views.plan_create, name='create'),
    path('<int:pk>/edit/', views.plan_edit, name='edit'),
]
