from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Include the main API urls from the backend root
    path('api/', include('urls')),
]
