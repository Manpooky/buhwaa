from rest_framework import viewsets
from .models import Country, Language, VisaType
from .serializers import CountrySerializer, LanguageSerializer, VisaTypeSerializer


class CountryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Country.objects.all().order_by('name')
    serializer_class = CountrySerializer


class LanguageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Language.objects.all().order_by('name')
    serializer_class = LanguageSerializer


class VisaTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = VisaType.objects.all().order_by('name')
    serializer_class = VisaTypeSerializer
    
    def get_queryset(self):
        queryset = VisaType.objects.all().order_by('name')
        country_code = self.request.query_params.get('country')
        if country_code:
            queryset = queryset.filter(countries__code=country_code)
        return queryset 