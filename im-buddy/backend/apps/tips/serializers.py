from rest_framework import serializers
from apps.visa_info.serializers import VisaTypeSerializer, LanguageSerializer
from .models import Tip


class TipSerializer(serializers.ModelSerializer):
    visa_type = VisaTypeSerializer(read_only=True)
    language = LanguageSerializer(read_only=True)
    
    class Meta:
        model = Tip
        fields = ['id', 'visa_type', 'content', 'language'] 