from django.urls import path
from .views import get_tips

urlpatterns = [
    path('', get_tips, name='get_tips'),
] 