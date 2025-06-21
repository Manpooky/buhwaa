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