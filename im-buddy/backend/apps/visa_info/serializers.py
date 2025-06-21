from rest_framework import serializers
from .models import Country, Language, VisaType


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['code', 'name']


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['code', 'name']


class VisaTypeSerializer(serializers.ModelSerializer):
    countries = CountrySerializer(many=True, read_only=True)
    
    class Meta:
        model = VisaType
        fields = ['code', 'name', 'description', 'countries'] 