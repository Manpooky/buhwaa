from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from django.http import FileResponse
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from apps.visa_info.models import Language
from .models import Translation, DocumentTranslation
from .serializers import TranslationSerializer, DocumentTranslationSerializer
from services.llama_service import translate_text
from services.pdf_service import extract_text_from_pdf, create_pdf_from_text


@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['text', 'source_language', 'target_language'],
        properties={
            'text': openapi.Schema(type=openapi.TYPE_STRING, description='Text to translate'),
            'source_language': openapi.Schema(type=openapi.TYPE_STRING, description='Source language code'),
            'target_language': openapi.Schema(type=openapi.TYPE_STRING, description='Target language code'),
        },
    ),
    responses={
        status.HTTP_200_OK: TranslationSerializer,
        status.HTTP_400_BAD_REQUEST: 'Bad request',
    },
    operation_description="Translate text from source language to target language",
)
@api_view(['POST'])
@permission_classes([AllowAny])
def translate(request):
    """
    Translate text from one language to another
    
    Requires:
    - text: The text to translate
    - source_language: Source language code (e.g., 'en', 'es')
    - target_language: Target language code
    """
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
    
    if request.user.is_authenticated:
        user = request.user
    else:
        from django.contrib.auth.models import User
        user = User.objects.get(username='test_user')
    # Save translation to database
    translation = Translation.objects.create(
        user=user,
        original_text=text,
        translated_text=translated_text,
        source_language=source_lang_obj,
        target_language=target_lang_obj
    )
    
    serializer = TranslationSerializer(translation)
    return Response(serializer.data)


@swagger_auto_schema(
    method='post',
    manual_parameters=[
        openapi.Parameter(
            'document', 
            openapi.IN_FORM,
            type=openapi.TYPE_FILE,
            required=True,
            description='PDF document to translate'
        ),
        openapi.Parameter(
            'source_language', 
            openapi.IN_FORM,
            type=openapi.TYPE_STRING,
            required=True,
            description='Source language code (e.g., "en")'
        ),
        openapi.Parameter(
            'target_language', 
            openapi.IN_FORM,
            type=openapi.TYPE_STRING,
            required=True,
            description='Target language code (e.g., "es")'
        ),
    ],
    responses={
        status.HTTP_200_OK: DocumentTranslationSerializer,
        status.HTTP_400_BAD_REQUEST: 'Bad request',
        status.HTTP_500_INTERNAL_SERVER_ERROR: 'Internal server error',
    },
    operation_description="Upload and translate a PDF document",
)
@api_view(['POST'])
@permission_classes([AllowAny])
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
        
        # Generate translated PDF from the text
        translated_file_name = f"translated_{document.name}"
        translated_pdf = create_pdf_from_text(translated_text, translated_file_name)
        
        # Update document translation with the result
        doc_translation.translated_text = translated_text
        doc_translation.translated_document.save(translated_file_name, translated_pdf)
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


@swagger_auto_schema(
    method='get',
    responses={
        status.HTTP_200_OK: DocumentTranslationSerializer,
        status.HTTP_404_NOT_FOUND: 'Translation not found',
    },
    operation_description="Get a specific document translation by ID",
)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_document_translation(request, doc_id):
    """
    Get a specific document translation by ID
    """
    translation = get_object_or_404(DocumentTranslation, id=doc_id, user=request.user)
    serializer = DocumentTranslationSerializer(translation)
    return Response(serializer.data)


@swagger_auto_schema(
    method='get',
    responses={
        status.HTTP_200_OK: openapi.Response(
            description="File download response",
            schema=openapi.Schema(type=openapi.TYPE_FILE)
        ),
        status.HTTP_404_NOT_FOUND: 'Translation not found',
        status.HTTP_400_BAD_REQUEST: 'Translation not complete',
    },
    operation_description="Download translated document as PDF",
)
@api_view(['GET'])
@permission_classes([AllowAny])
def download_translated_document(request, doc_id):
    """
    Download a translated document as a PDF file
    """
    translation = get_object_or_404(DocumentTranslation, id=doc_id, user=request.user)
    
    if not translation.translated_document:
        # If the translated document is not available, generate it on the fly
        if translation.translated_text:
            translated_file_name = f"translated_{translation.file_name}"
            translated_pdf = create_pdf_from_text(translation.translated_text, translated_file_name)
            translation.translated_document.save(translated_file_name, translated_pdf)
            translation.save()
        else:
            return Response(
                {'error': 'Translation is not complete or failed'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    # Open the file and create a FileResponse
    response = FileResponse(
        translation.translated_document.open('rb'),
        content_type='application/pdf'
    )
    
    # Set the content-disposition header to make the file downloadable
    filename = translation.translated_document.name.split('/')[-1]
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response


@swagger_auto_schema(
    method='get',
    responses={
        status.HTTP_200_OK: DocumentTranslationSerializer(many=True),
    },
    operation_description="List all document translations for the current user",
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_document_translations(request):
    """
    List all document translations for the current user
    """
    translations = DocumentTranslation.objects.filter(user=request.user).order_by('-created_at')
    serializer = DocumentTranslationSerializer(translations, many=True)
    return Response(serializer.data) 