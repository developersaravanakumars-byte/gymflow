from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('accounts.urls')),
    path('dashboard/', include('members.urls')),
    path('enquiries/', include('enquiries.urls')),
    path('plans/', include('plans.urls')),
    path('payments/', include('payments.urls')),
    path('branches/', include('branches.urls')),
    path('reports/', include('reports.urls')),
    path('', RedirectView.as_view(url='/dashboard/', permanent=False)),
]
