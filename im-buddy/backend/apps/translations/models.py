from django.db import models
from django.contrib.auth.models import User
from apps.visa_info.models import Language


class Translation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    original_text = models.TextField()
    translated_text = models.TextField()
    source_language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='source_translations')
    target_language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='target_translations')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Translation from {self.source_language} to {self.target_language}"


def document_original_path(instance, filename):
    """
    Generate path for original document files
    """
    # Organize by user ID and file type
    return f'documents/original/user_{instance.user.id}/{filename}'


def document_translated_path(instance, filename):
    """
    Generate path for translated document files
    """
    # Organize by user ID and file type
    return f'documents/translated/user_{instance.user.id}/{filename}'


class DocumentTranslation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    original_document = models.FileField(upload_to=document_original_path)
    translated_document = models.FileField(upload_to=document_translated_path, blank=True, null=True)
    original_text = models.TextField()
    translated_text = models.TextField()
    source_language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='source_document_translations')
    target_language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='target_document_translations')
    created_at = models.DateTimeField(auto_now_add=True)
    file_name = models.CharField(max_length=255)
    status = models.CharField(max_length=20, default='processing', 
                             choices=[
                                 ('processing', 'Processing'),
                                 ('completed', 'Completed'),
                                 ('failed', 'Failed')
                             ])
    
    def __str__(self):
        return f"Document translation: {self.file_name} from {self.source_language} to {self.target_language}" 