from django.db import models
from apps.visa_info.models import VisaType, Language


class Tip(models.Model):
    visa_type = models.ForeignKey(VisaType, on_delete=models.CASCADE, related_name='tips')
    content = models.TextField()
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Tip for {self.visa_type} in {self.language}" 