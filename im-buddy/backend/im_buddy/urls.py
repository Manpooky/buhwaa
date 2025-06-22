from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Create Swagger schema view
schema_view = get_schema_view(
    openapi.Info(
        title="IM-Buddy API",
        default_version='v1',
        description="API documentation for IM-Buddy application",
        terms_of_service="https://www.yourapp.com/terms/",
        contact=openapi.Contact(email="contact@yourapp.com"),
        license=openapi.License(name="Your License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # Include the main API urls from the backend root
    path('api/', include('urls')),
    
    # API Documentation with Swagger
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# Add debug toolbar URLs if in debug mode
if settings.DEBUG:
    urlpatterns += [
        # Serve media files in development
        *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    ]
