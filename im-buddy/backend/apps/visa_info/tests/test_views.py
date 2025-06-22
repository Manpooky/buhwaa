from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from apps.visa_info.models import Country, Language, VisaType


class VisaInfoModelTests(TestCase):
    """Test case for visa info models only"""
    
    def setUp(self):
        """Set up objects used by all test methods."""
        # Create countries
        self.usa = Country.objects.create(name="United States", code="US")
        self.japan = Country.objects.create(name="Japan", code="JP")
        
        # Create languages
        self.english = Language.objects.create(name="English", code="en")
        self.japanese = Language.objects.create(name="Japanese", code="ja")
        
        # Create visa types
        self.tourist_visa = VisaType.objects.create(
            code="TOURIST",
            name="Tourist Visa",
            description="For tourism purposes"
        )
        self.tourist_visa.countries.add(self.japan)
    
    def test_country_str(self):
        """Test the string representation of a country"""
        self.assertEqual(str(self.usa), "United States")
        
    def test_language_str(self):
        """Test the string representation of a language"""
        self.assertEqual(str(self.english), "English")
        
    def test_visa_type_str(self):
        """Test the string representation of a visa type"""
        self.assertEqual(str(self.tourist_visa), "Tourist Visa")
        
    def test_visa_type_countries(self):
        """Test the countries related to a visa type"""
        self.assertEqual(self.tourist_visa.countries.count(), 1)
        self.assertEqual(self.tourist_visa.countries.first(), self.japan) 