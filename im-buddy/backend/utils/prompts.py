"""
Llama 4 Prompt Templates for Immigration Form Translation System
"""

from typing import Dict, Any, List, Optional
import json
import logging
from datetime import datetime

class ImmigrationFormPrompts:
    """
    Centralized prompt management for immigration form translation
    """

    @staticmethod
    def phase1_translation_prompt(
            form_content: str,
            form_fields: List[Dict[str, Any]],
            form_metadata: Dict[str, Any],
            target_language: str,
            original_language: Optional[str] = None
    ) -> str:
        """
        Phase 1: Translate foreign immigration form to user's language
        """

        language_context = f"from {original_language} " if original_language else ""

        return f"""
IMMIGRATION FORM TRANSLATION - PHASE 1
{language_context}to {target_language}

=== ORIGINAL FORM CONTENT ===
{form_content}

=== FORM STRUCTURE ===
Total Pages: {form_metadata.get('total_pages', 'Unknown')}
Document Title: {form_metadata.get('title', 'Immigration Form')}

Form Fields Detected:
{json.dumps(form_fields, indent=2)}

=== TRANSLATION REQUIREMENTS ===

TARGET LANGUAGE: {target_language}

CRITICAL INSTRUCTIONS:
1. **COMPLETE TRANSLATION**: Translate ALL text content to {target_language}
2. **PRESERVE STRUCTURE**: Maintain exact formatting, spacing, and layout
3. **FIELD INTEGRITY**: Keep field names/IDs unchanged for technical compatibility
4. **LEGAL ACCURACY**: Use official immigration terminology in {target_language}
5. **CULTURAL ADAPTATION**: Use appropriate date formats and conventions for {target_language}

SPECIFIC TRANSLATION GUIDELINES:
- Form titles and headers: Translate completely
- Field labels and descriptions: Translate with legal precision
- Instructions and help text: Make clear and understandable in {target_language}
- Legal disclaimers: Use official legal language
- Country/place names: Use standard {target_language} conventions
- Dates: Show both original format and {target_language} format explanation
- Numbers: Use appropriate decimal/thousand separators for {target_language}

TECHNICAL REQUIREMENTS:
- Preserve all form field positioning and structure
- Maintain checkbox, radio button, and dropdown functionality
- Keep validation rules intact
- Preserve any conditional logic between fields

QUALITY STANDARDS:
- Immigration-level accuracy required
- Professional, formal tone
- Consistent terminology throughout
- Clear, unambiguous language
- Accessible to non-native speakers

OUTPUT FORMAT:
Return the complete translated form maintaining the original PDF structure, followed by:

FIELD MAPPING TABLE:
Original Field Label → Translated Label (Technical Field Name)

TRANSLATION NOTES:
- Any complex terms that needed special consideration
- Cultural adaptations made
- Format changes for {target_language} conventions
"""

    @staticmethod
    def phase2_reverse_translation_prompt(
            original_form_structure: Dict[str, Any],
            user_inputs: Dict[str, Any],
            user_language: str,
            target_country: Optional[str] = None
    ) -> str:
        """
        Phase 2: Translate user inputs back to original form language
        """

        country_context = f" for {target_country}" if target_country else ""

        return f"""
IMMIGRATION FORM TRANSLATION - PHASE 2
Reverse Translation: {user_language} → Original Language{country_context}

=== ORIGINAL FORM STRUCTURE ===
{json.dumps(original_form_structure, indent=2)}

=== USER INPUT DATA (in {user_language}) ===
{json.dumps(user_inputs, indent=2)}

Form Completion Status: {user_inputs.get('completion_percentage', 'Unknown')}%
Filled Fields: {len(user_inputs.get('filled_fields', {}))}
Empty Fields: {user_inputs.get('empty_fields', [])}

=== REVERSE TRANSLATION REQUIREMENTS ===

CRITICAL OBJECTIVES:
1. **PERFECT MAPPING**: Map each user input to correct original form field
2. **LINGUISTIC ACCURACY**: Translate user data to original form language
3. **LEGAL COMPLIANCE**: Ensure translations meet official standards{country_context}
4. **DATA INTEGRITY**: Preserve all user information accurately
5. **FORMAT COMPLIANCE**: Match original country's data formats

TRANSLATION GUIDELINES:

PERSONAL INFORMATION:
- Names: Keep as entered unless transliteration required
- Addresses: Translate descriptive parts, preserve proper nouns
- Dates: Convert to destination country format (DD/MM/YYYY vs MM/DD/YYYY)
- Phone numbers: Maintain international format with country codes
- Email addresses: Keep unchanged

OFFICIAL DATA:
- Document numbers: Keep exactly as entered
- Reference numbers: Preserve formatting
- Official titles: Use precise official translations
- Government agencies: Use official names in original language

DESCRIPTIVE TEXT:
- Employment descriptions: Use professional terminology
- Education details: Use academic equivalents
- Personal statements: Maintain meaning while using formal language
- Reasons/explanations: Use appropriate legal/official language

VALIDATION REQUIREMENTS:
- Cross-reference related fields for consistency
- Ensure required fields are completed
- Validate data formats match original form requirements
- Check conditional logic is satisfied

COUNTRY-SPECIFIC FORMATTING{country_context}:
- Date formats: Use standard format for destination country
- Address formats: Follow postal conventions
- Phone formats: Use national numbering conventions
- Currency: Use appropriate currency codes and formats
- Measurement units: Convert if necessary (metric/imperial)

DATA QUALITY CHECKS:
- Verify completeness of required fields
- Flag any inconsistencies in user data
- Note any fields that may need additional documentation
- Identify potential issues for manual review

OUTPUT REQUIREMENTS:
1. Complete form in original language with all user data properly inserted
2. Data validation report highlighting any issues
3. Translation accuracy notes for critical fields
4. Recommendations for any missing information

FINAL FORM: Return the completed immigration form in the original language, ready for official submission.
"""

    @staticmethod
    def language_detection_prompt(text_sample: str) -> str:
        """
        Detect the language of a document
        """
        return f"""
LANGUAGE DETECTION FOR IMMIGRATION DOCUMENT

TEXT SAMPLE:
{text_sample}

TASK: Identify the primary language of this immigration document.

INSTRUCTIONS:
1. Analyze the text sample for language patterns
2. Consider immigration document terminology
3. Look for country-specific legal language
4. Identify any mixed languages (note all present)

RETURN FORMAT:
Primary Language: [Language Name]
Confidence: [High/Medium/Low]
Secondary Languages: [If any detected]
Country Context: [If identifiable from legal terminology]

Focus on immigration and legal document context for accurate identification.
"""

    @staticmethod
    def field_extraction_prompt(form_content: str) -> str:
        """
        Extract and analyze form fields from document
        """
        return f"""
IMMIGRATION FORM FIELD ANALYSIS

DOCUMENT CONTENT:
{form_content}

ANALYSIS TASK: Extract and categorize all form fields from this immigration document.

EXTRACTION REQUIREMENTS:
1. **IDENTIFY ALL FIELDS**: Find every input field, checkbox, dropdown, text area
2. **CATEGORIZE BY TYPE**: text, number, date, select, checkbox, radio, textarea
3. **DETERMINE REQUIREMENTS**: required vs optional fields
4. **EXTRACT VALIDATION**: format requirements, length limits, allowed values
5. **MAP RELATIONSHIPS**: conditional fields, dependent sections
6. **IDENTIFY SECTIONS**: group related fields logically

FIELD ANALYSIS FORMAT:
For each field, provide:
- field_id: unique identifier
- field_label: user-visible label
- field_type: input type (text/number/date/select/checkbox/etc.)
- required: true/false
- validation_rules: format requirements
- conditional_logic: dependencies on other fields
- section: which part of form it belongs to
- options: for select/radio fields
- help_text: any explanatory text
- legal_importance: critical/important/standard

SECTION ANALYSIS:
Group fields into logical sections:
- Personal Information
- Contact Details
- Immigration History
- Employment Information
- Family Information
- Supporting Documents
- Declarations/Signatures

COMPLEXITY ASSESSMENT:
- Total field count
- Required field count
- Conditional logic complexity
- Estimated completion time
- Difficulty level (1-10)

OUTPUT: Structured JSON with complete field analysis and form metadata.
"""

    @staticmethod
    def user_input_extraction_prompt(
            original_fields: List[Dict[str, Any]],
            filled_form_content: str,
            user_language: str
    ) -> str:
        """
        Extract user inputs from filled form
        """
        return f"""
USER INPUT EXTRACTION FROM FILLED FORM

ORIGINAL FORM FIELDS:
{json.dumps(original_fields, indent=2)}

FILLED FORM CONTENT (in {user_language}):
{filled_form_content}

EXTRACTION TASK: Extract all user-provided data from the filled form.

EXTRACTION REQUIREMENTS:
1. **MAP TO ORIGINAL FIELDS**: Match user inputs to original field structure
2. **PRESERVE EXACT VALUES**: Extract user data without modification
3. **IDENTIFY EMPTY FIELDS**: Note which required fields are unfilled
4. **VALIDATE FORMATS**: Check if user inputs match expected formats
5. **EXTRACT SIGNATURES**: Identify signature fields and status

EXTRACTION PROCESS:
1. Scan for field labels and associated user inputs
2. Map each input to corresponding original field
3. Extract exact user-entered values
4. Note any validation issues
5. Calculate completion percentage

OUTPUT FORMAT:
{{
    "filled_fields": {{
        "field_id": "user_entered_value",
        ...
    }},
    "empty_fields": ["field_id1", "field_id2"],
    "validation_issues": [
        {{
            "field_id": "field_name",
            "issue": "description",
            "user_value": "what_user_entered",
            "expected_format": "required_format"
        }}
    ],
    "completion_percentage": 85,
    "signatures_present": true/false,
    "form_ready_for_submission": true/false,
    "missing_required_fields": ["field_id1", "field_id2"]
}}

VALIDATION CHECKS:
- Required field completeness
- Date format validation
- Email format validation
- Phone number format validation
- Document number format validation
- Conditional field logic satisfaction
"""

    @staticmethod
    def translation_quality_check_prompt(
            original_text: str,
            translated_text: str,
            source_language: str,
            target_language: str
    ) -> str:
        """
        Quality check for translations
        """
        return f"""
TRANSLATION QUALITY ASSESSMENT

SOURCE ({source_language}):
{original_text}

TRANSLATION ({target_language}):
{translated_text}

QUALITY ASSESSMENT TASK: Evaluate the translation quality for immigration document standards.

ASSESSMENT CRITERIA:
1. **ACCURACY**: Meaning preservation and correctness
2. **LEGAL TERMINOLOGY**: Proper use of immigration/legal terms
3. **COMPLETENESS**: No missing information
4. **FORMALITY**: Appropriate formal/official tone
5. **CULTURAL ADAPTATION**: Proper localization for target language
6. **CONSISTENCY**: Uniform terminology throughout

EVALUATION AREAS:

LINGUISTIC QUALITY:
- Grammar and syntax correctness
- Natural language flow
- Proper vocabulary choice
- Sentence structure appropriateness

LEGAL ACCURACY:
- Immigration terminology precision
- Legal concept translation accuracy
- Official language compliance
- Regulatory terminology consistency

FUNCTIONAL COMPLETENESS:
- All information translated
- Field labels clearly understood
- Instructions comprehensible
- No ambiguous translations

ASSESSMENT OUTPUT:
{{
    "overall_quality": "Excellent/Good/Fair/Poor",
    "accuracy_score": "1-10",
    "legal_terminology_score": "1-10",
    "completeness_score": "1-10",
    "issues_found": [
        {{
            "severity": "High/Medium/Low",
            "location": "where in text",
            "issue": "description",
            "suggested_improvement": "recommendation"
        }}
    ],
    "approval_status": "Approved/Needs_Review/Requires_Revision",
    "reviewer_notes": "additional comments"
}}

RECOMMENDATION: Provide overall assessment and improvement suggestions.
"""

    @staticmethod
    def get_prompt_by_phase(
            phase: str,
            **kwargs
    ) -> str:
        """
        Dispatcher method to get prompts by phase
        """
        prompt_map = {
            "phase1": ImmigrationFormPrompts.phase1_translation_prompt,
            "phase2": ImmigrationFormPrompts.phase2_reverse_translation_prompt,
            "language_detection": ImmigrationFormPrompts.language_detection_prompt,
            "field_extraction": ImmigrationFormPrompts.field_extraction_prompt,
            "input_extraction": ImmigrationFormPrompts.user_input_extraction_prompt,
            "quality_check": ImmigrationFormPrompts.translation_quality_check_prompt
        }

        if phase not in prompt_map:
            raise ValueError(f"Unknown phase: {phase}. Available: {list(prompt_map.keys())}")

        return prompt_map[phase](**kwargs)


class PromptManager:
    """
    Manages prompt execution, logging, and optimization
    """

    def __init__(self, log_prompts: bool = True):
        self.prompts = ImmigrationFormPrompts()
        self.log_prompts = log_prompts

        if log_prompts:
            logging.basicConfig(level=logging.INFO)
            self.logger = logging.getLogger(__name__)

    def prepare_prompt(
            self,
            phase: str,
            context: Dict[str, Any],
            optimization_level: str = "standard"
    ) -> Dict[str, Any]:
        """
        Prepare a prompt with proper context and settings
        """
        try:
            from .prompt_config import PromptConfig
            config = PromptConfig()

            # Get the prompt text
            prompt_text = self.prompts.get_prompt_by_phase(phase, **context)

            # Get optimal settings for this prompt type
            settings = config.get_settings(phase)

            # Apply optimization
            if optimization_level == "high_accuracy":
                settings["temperature"] = max(0.1, settings["temperature"] - 0.1)
            elif optimization_level == "creative":
                settings["temperature"] = min(0.7, settings["temperature"] + 0.2)

            prompt_package = {
                "prompt": prompt_text,
                "settings": settings,
                "phase": phase,
                "context": context,
                "timestamp": datetime.now().isoformat()
            }

            if self.log_prompts:
                self.logger.info(f"Prepared prompt for phase: {phase}")

            return prompt_package

        except Exception as e:
            if self.log_prompts:
                self.logger.error(f"Error preparing prompt for phase {phase}: {str(e)}")
            raise

    def log_prompt_execution(
            self,
            prompt_package: Dict[str, Any],
            response: str,
            execution_time: float,
            token_usage: Optional[int] = None
    ):
        """
        Log prompt execution for analysis and optimization
        """
        if not self.log_prompts:
            return

        log_entry = {
            "phase": prompt_package["phase"],
            "execution_time": execution_time,
            "token_usage": token_usage,
            "response_length": len(response),
            "timestamp": datetime.now().isoformat(),
            "success": True
        }

        self.logger.info(f"Prompt executed: {json.dumps(log_entry)}")

    def optimize_prompt_for_language(
            self,
            prompt_text: str,
            target_language: str
    ) -> str:
        """
        Optimize prompt based on target language characteristics
        """
        try:
            from .prompt_config import PromptConfig
            config = PromptConfig()

            lang_info = config.get_language_info(target_language)

            # Add language-specific instructions
            if lang_info.get("rtl"):
                prompt_text += f"\n\nSPECIAL NOTE: {target_language} is a right-to-left language. Ensure proper text direction and formatting."

            # Add date format instructions
            date_format = lang_info.get("date_format", "DD/MM/YYYY")
            prompt_text += f"\n\nDATE FORMAT: Use {date_format} format for all dates in {target_language}."

            return prompt_text
        except ImportError:
            # Fallback if config not available
            return prompt_text