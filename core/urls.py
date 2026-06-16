from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # This securely hooks up your core routing to your portal app routes
    path('', include('portal.urls')), 
]
