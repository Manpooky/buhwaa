import os
import time
import uuid
from urllib.parse import urljoin

from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
from django.conf import settings

from .supabase_client import get_client

@deconstructible
class SupabaseStorage(Storage):
    """
    Custom Django storage backend for Supabase
    """
    
    def __init__(self, bucket_name='documents', base_url=None):
        """
        Initialize Supabase storage backend
        
        Args:
            bucket_name (str): Supabase storage bucket name
            base_url (str): Base URL for file access
        """
        self.bucket_name = bucket_name
        self.supabase = get_client()
        self.base_url = base_url or os.getenv("SUPABASE_URL") + "/storage/v1/object/public/"
    
    def _get_unique_filename(self, name):
        """
        Generate a unique filename to avoid collisions
        
        Args:
            name (str): Original filename
        
        Returns:
            str: Unique filename
        """
        ext = os.path.splitext(name)[1] if name else ''
        filename = f"{uuid.uuid4().hex}{ext}"
        return filename
    
    def _open(self, name, mode='rb'):
        """
        Not implemented - Supabase doesn't support direct file opening
        """
        raise NotImplementedError("Supabase storage doesn't support direct file opening")
    
    def _save(self, name, content):
        """
        Save file to Supabase storage
        
        Args:
            name (str): File path
            content (File): File content
        
        Returns:
            str: Saved file path
        """
        # Get a unique filename
        unique_name = self._get_unique_filename(name)
        
        # Create a folder structure based on date
        path = f"{time.strftime('%Y/%m/%d')}/{unique_name}"
        
        # Upload the file to Supabase
        try:
            self.supabase.storage.from_(self.bucket_name).upload(
                path,
                content.read(),
                {"content-type": content.content_type if hasattr(content, 'content_type') else None}
            )
        except Exception as e:
            raise IOError(f"Failed to save file to Supabase storage: {e}")
        
        return path
    
    def url(self, name):
        """
        Get URL for accessing the file
        
        Args:
            name (str): File path
        
        Returns:
            str: Public URL for the file
        """
        return urljoin(urljoin(self.base_url, self.bucket_name + '/'), name)
    
    def exists(self, name):
        """
        Check if a file exists
        
        Args:
            name (str): File path
        
        Returns:
            bool: True if file exists
        """
        try:
            response = self.supabase.storage.from_(self.bucket_name).list()
            files = [item['name'] for item in response]
            return name in files
        except:
            return False
    
    def delete(self, name):
        """
        Delete a file
        
        Args:
            name (str): File path
        """
        try:
            self.supabase.storage.from_(self.bucket_name).remove([name])
        except Exception as e:
            pass  # Silently ignore errors
    
    def size(self, name):
        """
        Get file size
        
        Args:
            name (str): File path
        
        Returns:
            int: File size in bytes
        """
        try:
            response = self.supabase.storage.from_(self.bucket_name).list()
            for item in response:
                if item['name'] == name:
                    return item['metadata'].get('size', 0)
            return 0
        except:
            return 0
    
    def get_accessed_time(self, name):
        """Not implemented for Supabase"""
        return None
    
    def get_created_time(self, name):
        """Not implemented for Supabase"""
        return None
    
    def get_modified_time(self, name):
        """Not implemented for Supabase"""
        return None 