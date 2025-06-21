from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404

from apps.visa_info.models import Language
from .models import Translation, DocumentTranslation
from .serializers import TranslationSerializer, DocumentTranslationSerializer
from services.llama_service import translate_text
from services.pdf_service import extract_text_from_pdf


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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def translate_document(request):
    """
    Endpoint for translating PDF documents
    
    Requires:
    - document: PDF file
    - source_language: language code
    - target_language: language code
    """
    # Validate request data
    if 'document' not in request.FILES:
        return Response(
            {'error': 'No document provided'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    document = request.FILES['document']
    source_language = request.data.get('source_language')
    target_language = request.data.get('target_language')
    
    if not source_language or not target_language:
        return Response(
            {'error': 'Missing language information'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Check file type
    if not document.name.lower().endswith('.pdf'):
        return Response(
            {'error': 'Only PDF files are supported'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    source_lang_obj = get_object_or_404(Language, code=source_language)
    target_lang_obj = get_object_or_404(Language, code=target_language)
    
    try:
        # Extract text from PDF
        extracted_text = extract_text_from_pdf(document)
        
        if not extracted_text or len(extracted_text.strip()) < 10:
            return Response(
                {'error': 'Could not extract text from the document'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create document translation record with processing status
        doc_translation = DocumentTranslation.objects.create(
            user=request.user,
            original_document=document,
            original_text=extracted_text,
            translated_text="",  # Will be updated after translation
            source_language=source_lang_obj,
            target_language=target_lang_obj,
            file_name=document.name,
            status='processing'
        )
        
        # Translate extracted text
        translated_text = translate_text(extracted_text, source_language, target_language)
        
        # Update document translation with the result
        doc_translation.translated_text = translated_text
        doc_translation.status = 'completed'
        doc_translation.save()
        
        # Return the translation data
        serializer = DocumentTranslationSerializer(doc_translation)
        return Response(serializer.data)
        
    except Exception as e:
        return Response(
            {'error': f'Error processing document: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_document_translation(request, doc_id):
    """
    Get a specific document translation by ID
    """
    translation = get_object_or_404(DocumentTranslation, id=doc_id, user=request.user)
    serializer = DocumentTranslationSerializer(translation)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_document_translations(request):
    """
    List all document translations for the current user
    """
    translations = DocumentTranslation.objects.filter(user=request.user).order_by('-created_at')
    serializer = DocumentTranslationSerializer(translations, many=True)
    return Response(serializer.data) 