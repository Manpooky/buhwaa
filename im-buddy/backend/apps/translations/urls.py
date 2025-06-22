from django.urls import path
from .views import translate, translate_document, get_document_translation, list_document_translations, download_translated_document

urlpatterns = [
    path('translate/', translate, name='translate'),
    path('document/translate/', translate_document, name='translate_document'),
    path('document/translations/', list_document_translations, name='list_document_translations'),
    path('document/translations/<int:doc_id>/', get_document_translation, name='get_document_translation'),
    path('document/translations/<int:doc_id>/download/', download_translated_document, name='download_translated_document'),
] 