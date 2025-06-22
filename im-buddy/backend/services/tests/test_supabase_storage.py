import unittest
from unittest.mock import patch, MagicMock
import tempfile
import os
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from services.supabase_storage import SupabaseStorage


class SupabaseStorageTest(TestCase):
    """Test case for Supabase storage service"""
    
    def setUp(self):
        """Set up test environment"""
        # Mock the Supabase client
        self.patcher = patch('services.supabase_storage.get_client')
        self.mock_get_client = self.patcher.start()
        self.mock_supabase = MagicMock()
        self.mock_get_client.return_value = self.mock_supabase
        
        # Create a temporary file for testing
        self.temp_dir = tempfile.mkdtemp()
        self.temp_file_path = os.path.join(self.temp_dir, "test.pdf")
        with open(self.temp_file_path, 'w') as f:
            f.write("Test file content")
        
        # Create the storage client
        self.storage = SupabaseStorage(bucket_name='test-bucket')
    
    def tearDown(self):
        """Clean up test environment"""
        self.patcher.stop()
        
        # Remove temporary files
        if os.path.exists(self.temp_file_path):
            os.remove(self.temp_file_path)
        os.rmdir(self.temp_dir)
    
    def test_url(self):
        """Test generating URLs for files"""
        # Test URL generation
        url = self.storage.url('test/file.pdf')
        self.assertTrue('test-bucket' in url)
        self.assertTrue('test/file.pdf' in url)
    
    @patch('services.supabase_storage.uuid.uuid4')
    def test_save(self, mock_uuid):
        """Test saving a file"""
        # Mock UUID generation
        mock_uuid.return_value = MagicMock(hex='1234567890abcdef')
        
        # Mock the storage client
        mock_bucket = MagicMock()
        self.mock_supabase.storage.from_.return_value = mock_bucket
        
        # Create a test file
        test_file = SimpleUploadedFile(
            "test.pdf", 
            b"file content", 
            content_type="application/pdf"
        )
        
        # Call _save method (through a patch to avoid actual file operations)
        with patch('builtins.open', MagicMock()), \
             patch('services.supabase_storage.time.strftime', return_value='2025/06/22'):
            path = self.storage._save('test.pdf', test_file)
        
        # Verify the file was uploaded with the correct parameters
        self.mock_supabase.storage.from_.assert_called_once_with('test-bucket')
        mock_bucket.upload.assert_called_once()
        
        # Check the path format
        self.assertEqual(path, '2025/06/22/1234567890abcdef.pdf') 