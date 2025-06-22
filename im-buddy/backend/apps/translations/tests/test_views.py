from django.test import TestCase, override_settings
from django.contrib.auth.models import User
from apps.translations.models import DocumentTranslation
from apps.visa_info.models import Language
from django.core.files.uploadedfile import SimpleUploadedFile
import tempfile
import os

# Use Django's default file storage for tests
@override_settings(DEFAULT_FILE_STORAGE='django.core.files.storage.FileSystemStorage')
class TranslationModelTests(TestCase):
    """Test case for translation models only"""
    
    def setUp(self):
        """Set up objects used by all test methods."""
        # Create user
        self.user = User.objects.create_user(
            username='testuser', 
            password='12345'
        )
        
        # Create language objects
        self.english = Language.objects.create(code='en', name='English')
        self.spanish = Language.objects.create(code='es', name='Spanish')
        
        # Create a sample PDF file
        sample_pdf = SimpleUploadedFile(
            "test_document.pdf", 
            b"file_content", 
            content_type="application/pdf"
        )
        
        # Create a document translation
        self.translation = DocumentTranslation.objects.create(
            user=self.user,
            original_document=sample_pdf,
            original_text="Hello world",
            translated_text="Hola mundo",
            source_language=self.english,
            target_language=self.spanish,
            file_name="test_document.pdf",
            status="completed"
        )
    
    def test_document_translation_str(self):
        """Test the string representation of a document translation"""
        expected = f"Document translation: test_document.pdf from {self.english} to {self.spanish}"
        self.assertEqual(str(self.translation), expected)
        
    def test_document_translation_fields(self):
        """Test the fields of a document translation"""
        self.assertEqual(self.translation.original_text, "Hello world")
        self.assertEqual(self.translation.translated_text, "Hola mundo")
        self.assertEqual(self.translation.source_language, self.english)
        self.assertEqual(self.translation.target_language, self.spanish)
        self.assertEqual(self.translation.file_name, "test_document.pdf")
        self.assertEqual(self.translation.status, "completed")
        
    def test_user_relationship(self):
        """Test that a document translation is related to a user"""
        self.assertEqual(self.translation.user, self.user) 