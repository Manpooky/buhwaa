from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from apps.visa_info.models import VisaType, Language
from .models import Tip
from .serializers import TipSerializer
from services.tips_service import generate_tips


@api_view(['GET'])
def get_tips(request):
    visa_type = request.query_params.get('visa_type')
    language = request.query_params.get('language', 'en')
    
    if not visa_type:
        return Response(
            {'error': 'Visa type is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    visa_type_obj = get_object_or_404(VisaType, code=visa_type)
    language_obj = get_object_or_404(Language, code=language)
    
    # Try to get existing tips
    tips = Tip.objects.filter(visa_type=visa_type_obj, language=language_obj)
    
    # If no tips exist, generate them
    if not tips:
        tips_content = generate_tips(visa_type, language)
        tip = Tip.objects.create(
            visa_type=visa_type_obj,
            content=tips_content,
            language=language_obj
        )
        tips = [tip]
    
    serializer = TipSerializer(tips, many=True)
    return Response(serializer.data) 