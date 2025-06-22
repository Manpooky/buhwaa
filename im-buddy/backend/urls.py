from django.urls import path, include

urlpatterns = [
    # API endpoints grouped by app
    path('visa-info/', include('apps.visa_info.urls')),
    path('translations/', include('apps.translations.urls')),
    # path('tips/', include('apps.tips.urls')),  # Removed for now
] 