from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CountryViewSet, LanguageViewSet, VisaTypeViewSet

router = DefaultRouter()
router.register(r'countries', CountryViewSet)
router.register(r'languages', LanguageViewSet)
router.register(r'visa-types', VisaTypeViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 