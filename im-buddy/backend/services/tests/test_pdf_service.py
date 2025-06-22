import unittest
from unittest.mock import patch, MagicMock
import tempfile
import os
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from services.pdf_service import extract_text_with_pypdf, create_pdf_from_text


class PDFServiceTest(TestCase):
    """Test case for PDF service functions"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_text = "This is a test document.\nIt has multiple lines.\nAnd paragraphs."
        
        # Create a temporary PDF file for testing
        self.temp_dir = tempfile.mkdtemp()
        self.temp_pdf_path = os.path.join(self.temp_dir, "test.pdf")
        with open(self.temp_pdf_path, 'w') as f:
            f.write("Test PDF content")
        
    def tearDown(self):
        """Clean up test environment"""
        # Remove temporary files
        if os.path.exists(self.temp_pdf_path):
            os.remove(self.temp_pdf_path)
        os.rmdir(self.temp_dir)
    
    @patch('services.pdf_service.PyPDF2.PdfReader')
    def test_extract_text_with_pypdf(self, mock_pdf_reader):
        """Test extracting text from a PDF file"""
        # Mock the PDF reader
        mock_reader_instance = MagicMock()
        mock_pdf_reader.return_value = mock_reader_instance
        
        # Mock pages
        page1 = MagicMock()
        page1.extract_text.return_value = "This is a test document."
        page2 = MagicMock()
        page2.extract_text.return_value = "It has multiple lines.\nAnd paragraphs."
        
        # Set up the mock reader to return our mock pages
        mock_reader_instance.pages = [page1, page2]
        
        # Call the function
        result = extract_text_with_pypdf(self.temp_pdf_path)
        
        # Assert the result - match exactly what the function returns
        expected_text = "This is a test document.\nIt has multiple lines.\nAnd paragraphs.\n"
        self.assertEqual(result, expected_text)
    
    def test_create_pdf_from_text(self):
        """Test creating a PDF file from text"""
        # Call the function
        pdf_file = create_pdf_from_text(self.test_text)
        
        # Assert the PDF file was created
        self.assertIsNotNone(pdf_file)
        self.assertTrue(len(pdf_file.read()) > 0) 