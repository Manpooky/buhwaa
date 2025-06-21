from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from apps.visa_info.models import Language
from .models import Translation
from .serializers import TranslationSerializer
from services.llama_service import translate_text


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def translate(request):
    text = request.data.get('text')
    source_language = request.data.get('source_language')
    target_language = request.data.get('target_language')
    
    if not text or not source_language or not target_language:
        return Response(
            {'error': 'Missing required fields'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    source_lang_obj = get_object_or_404(Language, code=source_language)
    target_lang_obj = get_object_or_404(Language, code=target_language)
    
    # Call translation service
    translated_text = translate_text(text, source_language, target_language)
    
    # Save translation to database
    translation = Translation.objects.create(
        user=request.user,
        original_text=text,
        translated_text=translated_text,
        source_language=source_lang_obj,
        target_language=target_lang_obj
    )
    
    serializer = TranslationSerializer(translation)
    return Response(serializer.data) 