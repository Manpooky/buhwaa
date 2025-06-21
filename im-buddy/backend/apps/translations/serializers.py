from rest_framework import serializers
from apps.visa_info.serializers import LanguageSerializer
from .models import Translation


class TranslationSerializer(serializers.ModelSerializer):
    source_language = LanguageSerializer(read_only=True)
    target_language = LanguageSerializer(read_only=True)
    
    class Meta:
        model = Translation
        fields = ['id', 'original_text', 'translated_text', 'source_language', 
                  'target_language', 'created_at'] 