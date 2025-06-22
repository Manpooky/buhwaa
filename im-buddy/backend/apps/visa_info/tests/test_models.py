from django.test import TestCase
from apps.visa_info.models import Country, Language, VisaType


class CountryModelTest(TestCase):
    """Test case for Country model"""
    
    @classmethod
    def setUpTestData(cls):
        """Set up non-modified objects used by all test methods."""
        # Create a country
        Country.objects.create(
            name="United States",
            code="US"
        )
    
    def test_country_creation(self):
        """Test that a country can be created"""
        country = Country.objects.get(code="US")
        self.assertEqual(country.name, "United States")
        self.assertEqual(country.code, "US")


class LanguageModelTest(TestCase):
    """Test case for Language model"""
    
    @classmethod
    def setUpTestData(cls):
        """Set up non-modified objects used by all test methods."""
        # Create a language
        Language.objects.create(
            name="English",
            code="en"
        )
    
    def test_language_creation(self):
        """Test that a language can be created"""
        language = Language.objects.get(code="en")
        self.assertEqual(language.name, "English")
        self.assertEqual(language.code, "en")


class VisaTypeModelTest(TestCase):
    """Test case for VisaType model"""
    
    @classmethod
    def setUpTestData(cls):
        """Set up non-modified objects used by all test methods."""
        # Create countries
        japan = Country.objects.create(name="Japan", code="JP")
        
        # Create visa type
        visa_type = VisaType.objects.create(
            code="TOURIST",
            name="Tourist Visa",
            description="Short-term visa for tourism purposes"
        )
        visa_type.countries.add(japan)
    
    def test_visa_type_creation(self):
        """Test that visa type can be created"""
        visa_type = VisaType.objects.get(code="TOURIST")
        self.assertEqual(visa_type.name, "Tourist Visa")
        self.assertEqual(visa_type.description, "Short-term visa for tourism purposes")
        self.assertEqual(visa_type.countries.count(), 1)
        self.assertEqual(visa_type.countries.first().name, "Japan") 