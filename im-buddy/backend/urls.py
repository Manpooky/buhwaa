from django.urls import path, include

urlpatterns = [
    path('', include('apps.visa_info.urls')),
    path('translations/', include('apps.translations.urls')),
    # path('tips/', include('apps.tips.urls')),  # Removed for now
] 