from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    
    # 🌟 SAFELY CONNECT THE APP: Routes all root traffic over to portal rules
    path("", include("portal.urls")),
]
