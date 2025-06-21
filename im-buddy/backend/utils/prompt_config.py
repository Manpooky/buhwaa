"""
Configuration and settings for prompt management
"""
from typing import List
from typing import Dict, Any

class PromptConfig:
    """Configuration settings for Llama 4 prompts"""

    # Model parameters for different prompt types
    PROMPT_SETTINGS = {
        "phase1_translation": {
            "temperature": 0.3,
            "max_tokens": 8000,
            "top_p": 0.9,
            "frequency_penalty": 0.0,
            "presence_penalty": 0.0
        },
        "phase2_translation": {
            "temperature": 0.2,  # Lower for accuracy
            "max_tokens": 6000,
            "top_p": 0.8,
            "frequency_penalty": 0.1,
            "presence_penalty": 0.0
        },
        "language_detection": {
            "temperature": 0.1,  # Very low for consistency
            "max_tokens": 500,
            "top_p": 0.7,
            "frequency_penalty": 0.0,
            "presence_penalty": 0.0
        },
        "field_extraction": {
            "temperature": 0.2,
            "max_tokens": 4000,
            "top_p": 0.8,
            "frequency_penalty": 0.0,
            "presence_penalty": 0.0
        },
        "input_extraction": {
            "temperature": 0.2,
            "max_tokens": 3000,
            "top_p": 0.8,
            "frequency_penalty": 0.0,
            "presence_penalty": 0.0
        },
        "quality_check": {
            "temperature": 0.3,
            "max_tokens": 2000,
            "top_p": 0.9,
            "frequency_penalty": 0.0,
            "presence_penalty": 0.0
        }
    }

    # Supported languages with their characteristics
    SUPPORTED_LANGUAGES = {
        "English": {"code": "en", "rtl": False, "date_format": "MM/DD/YYYY"},
        "Spanish": {"code": "es", "rtl": False, "date_format": "DD/MM/YYYY"},
        "French": {"code": "fr", "rtl": False, "date_format": "DD/MM/YYYY"},
        "German": {"code": "de", "rtl": False, "date_format": "DD.MM.YYYY"},
        "Italian": {"code": "it", "rtl": False, "date_format": "DD/MM/YYYY"},
        "Portuguese": {"code": "pt", "rtl": False, "date_format": "DD/MM/YYYY"},
        "Russian": {"code": "ru", "rtl": False, "date_format": "DD.MM.YYYY"},
        "Chinese": {"code": "zh", "rtl": False, "date_format": "YYYY/MM/DD"},
        "Japanese": {"code": "ja", "rtl": False, "date_format": "YYYY/MM/DD"},
        "Korean": {"code": "ko", "rtl": False, "date_format": "YYYY.MM.DD"},
        "Arabic": {"code": "ar", "rtl": True, "date_format": "DD/MM/YYYY"},
        "Hebrew": {"code": "he", "rtl": True, "date_format": "DD/MM/YYYY"},
        "Hindi": {"code": "hi", "rtl": False, "date_format": "DD/MM/YYYY"},
        "Turkish": {"code": "tr", "rtl": False, "date_format": "DD.MM.YYYY"},
        "Dutch": {"code": "nl", "rtl": False, "date_format": "DD-MM-YYYY"},
        "Polish": {"code": "pl", "rtl": False, "date_format": "DD.MM.YYYY"},
        "Czech": {"code": "cs", "rtl": False, "date_format": "DD.MM.YYYY"},
        "Swedish": {"code": "sv", "rtl": False, "date_format": "YYYY-MM-DD"},
        "Norwegian": {"code": "no", "rtl": False, "date_format": "DD.MM.YYYY"},
        "Danish": {"code": "da", "rtl": False, "date_format": "DD.MM.YYYY"}
    }

    # Country-specific immigration contexts
    COUNTRY_CONTEXTS = {
        "United States": {
            "date_format": "MM/DD/YYYY",
            "agency": "USCIS",
            "common_forms": ["I-485", "I-130", "I-140", "N-400"],
            "address_format": "US"
        },
        "Canada": {
            "date_format": "DD/MM/YYYY",
            "agency": "IRCC",
            "common_forms": ["IMM-1344", "IMM-0008", "IMM-5406"],
            "address_format": "CA"
        },
        "United Kingdom": {
            "date_format": "DD/MM/YYYY",
            "agency": "Home Office",
            "common_forms": ["VAF", "FLR", "SET"],
            "address_format": "UK"
        },
        "Australia": {
            "date_format": "DD/MM/YYYY",
            "agency": "Department of Home Affairs",
            "common_forms": ["47SP", "40SP", "80"],
            "address_format": "AU"
        },
        "Germany": {
            "date_format": "DD.MM.YYYY",
            "agency": "BAMF",
            "common_forms": ["Antrag", "Anlage"],
            "address_format": "DE"
        },
        "France": {
            "date_format": "DD/MM/YYYY",
            "agency": "OFII",
            "common_forms": ["CERFA", "Demande"],
            "address_format": "FR"
        },
        "Netherlands": {
            "date_format": "DD-MM-YYYY",
            "agency": "IND",
            "common_forms": ["Aanvraag", "Formulier"],
            "address_format": "NL"
        },
        "Sweden": {
            "date_format": "YYYY-MM-DD",
            "agency": "Migrationsverket",
            "common_forms": ["Ansökan", "Blankett"],
            "address_format": "SE"
        }
    }

    @classmethod
    def get_settings(cls, prompt_type: str) -> Dict[str, Any]:
        """Get settings for a specific prompt type"""
        # Map phase names to settings
        phase_mapping = {
            "phase1": "phase1_translation",
            "phase2": "phase2_translation",
            "language_detection": "language_detection",
            "field_extraction": "field_extraction",
            "input_extraction": "input_extraction",
            "quality_check": "quality_check"
        }

        settings_key = phase_mapping.get(prompt_type, prompt_type)
        return cls.PROMPT_SETTINGS.get(settings_key, cls.PROMPT_SETTINGS["phase1_translation"])

    @classmethod
    def get_language_info(cls, language: str) -> Dict[str, Any]:
        """Get information about a specific language"""
        return cls.SUPPORTED_LANGUAGES.get(language, cls.SUPPORTED_LANGUAGES["English"])

    @classmethod
    def get_country_info(cls, country: str) -> Dict[str, Any]:
        """Get country-specific immigration context"""
        return cls.COUNTRY_CONTEXTS.get(country, {})

    @classmethod
    def get_all_supported_languages(cls) -> List[str]:
        """Get list of all supported languages"""
        return list(cls.SUPPORTED_LANGUAGES.keys())

    @classmethod
    def get_all_supported_countries(cls) -> List[str]:
        """Get list of all supported countries"""
        return list(cls.COUNTRY_CONTEXTS.keys())

    @classmethod
    def is_rtl_language(cls, language: str) -> bool:
        """Check if a language is right-to-left"""
        lang_info = cls.get_language_info(language)
        return lang_info.get("rtl", False)

    @classmethod
    def get_date_format(cls, language: str) -> str:
        """Get the preferred date format for a language"""
        lang_info = cls.get_language_info(language)
        return lang_info.get("date_format", "DD/MM/YYYY")