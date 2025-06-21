# test_utilities.py
"""
Test script to verify the prompt utilities are working correctly
"""

import os
import sys
from datetime import datetime

def test_imports():
    """Test that all utilities can be imported"""
    print("🔄 Testing imports...")

    try:
        from utils.prompts import ImmigrationFormPrompts, PromptManager
        from utils.prompt_config import PromptConfig
        print("✅ All utilities imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you're running this from the correct directory and utils/ folder exists")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_prompt_generation():
    """Test prompt generation functionality"""
    print("\n🔄 Testing prompt generation...")

    try:
        from utils.prompts import ImmigrationFormPrompts

        # Test language detection prompt
        test_text = "Hello, this is a test immigration document. Antrag auf Aufenthaltserlaubnis."
        lang_prompt = ImmigrationFormPrompts.language_detection_prompt(test_text)

        if len(lang_prompt) > 100 and "LANGUAGE DETECTION" in lang_prompt:
            print("✅ Language detection prompt generated successfully")
        else:
            print("❌ Language detection prompt seems invalid")
            return False

        # Test phase1 prompt
        test_context = {
            "form_content": "Sample form content",
            "form_fields": [{"name": "test_field", "type": "text"}],
            "form_metadata": {"total_pages": 1, "title": "Test Form"},
            "target_language": "English"
        }

        phase1_prompt = ImmigrationFormPrompts.phase1_translation_prompt(**test_context)

        if len(phase1_prompt) > 500 and "IMMIGRATION FORM TRANSLATION - PHASE 1" in phase1_prompt:
            print("✅ Phase 1 prompt generated successfully")
        else:
            print("❌ Phase 1 prompt seems invalid")
            return False

        print("✅ Prompt generation working correctly")
        return True

    except Exception as e:
        print(f"❌ Prompt generation error: {e}")
        return False

def test_configuration():
    """Test configuration functionality"""
    print("\n🔄 Testing configuration...")

    try:
        from utils.prompt_config import PromptConfig

        config = PromptConfig()

        # Test settings retrieval
        settings = config.get_settings("phase1_translation")
        if isinstance(settings, dict) and "temperature" in settings:
            print("✅ Settings retrieval working")
        else:
            print("❌ Settings retrieval failed")
            return False

        # Test language info
        lang_info = config.get_language_info("German")
        if isinstance(lang_info, dict) and "date_format" in lang_info:
            print("✅ Language info retrieval working")
        else:
            print("❌ Language info retrieval failed")
            return False

        # Test supported languages
        languages = config.get_all_supported_languages()
        if isinstance(languages, list) and len(languages) > 10:
            print(f"✅ Found {len(languages)} supported languages")
        else:
            print("❌ Supported languages list seems invalid")
            return False

        print("✅ Configuration working correctly")
        return True

    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def test_prompt_manager():
    """Test prompt manager functionality"""
    print("\n🔄 Testing prompt manager...")

    try:
        from utils.prompts import PromptManager

        manager = PromptManager(log_prompts=False)  # Disable logging for test

        # Test prompt preparation
        context = {
            "text_sample": "Test document content"
        }

        prompt_package = manager.prepare_prompt("language_detection", context)

        if isinstance(prompt_package, dict) and "prompt" in prompt_package and "settings" in prompt_package:
            print("✅ Prompt preparation working")
        else:
            print("❌ Prompt preparation failed")
            return False

        # Test optimization levels
        high_accuracy_package = manager.prepare_prompt("language_detection", context, "high_accuracy")
        if high_accuracy_package["settings"]["temperature"] <= prompt_package["settings"]["temperature"]:
            print("✅ Optimization levels working")
        else:
            print("❌ Optimization levels not working correctly")
            return False

        print("✅ Prompt manager working correctly")
        return True

    except Exception as e:
        print(f"❌ Prompt manager error: {e}")
        return False

def test_dispatcher():
    """Test the prompt dispatcher functionality"""
    print("\n🔄 Testing prompt dispatcher...")

    try:
        from utils.prompts import ImmigrationFormPrompts

        # Test all available phases
        phases = ["phase1", "phase2", "language_detection", "field_extraction", "input_extraction", "quality_check"]

        for phase in phases:
            try:
                if phase == "phase1":
                    prompt = ImmigrationFormPrompts.get_prompt_by_phase(
                        phase,
                        form_content="test",
                        form_fields=[],
                        form_metadata={},
                        target_language="English"
                    )
                elif phase == "phase2":
                    prompt = ImmigrationFormPrompts.get_prompt_by_phase(
                        phase,
                        original_form_structure={},
                        user_inputs={},
                        user_language="English"
                    )
                elif phase == "language_detection":
                    prompt = ImmigrationFormPrompts.get_prompt_by_phase(
                        phase,
                        text_sample="test content"
                    )
                elif phase == "field_extraction":
                    prompt = ImmigrationFormPrompts.get_prompt_by_phase(
                        phase,
                        form_content="test content"
                    )
                elif phase == "input_extraction":
                    prompt = ImmigrationFormPrompts.get_prompt_by_phase(
                        phase,
                        original_fields=[],
                        filled_form_content="test",
                        user_language="English"
                    )
                elif phase == "quality_check":
                    prompt = ImmigrationFormPrompts.get_prompt_by_phase(
                        phase,
                        original_text="test",
                        translated_text="test",
                        source_language="German",
                        target_language="English"
                    )

                if len(prompt) > 50:
                    print(f"✅ {phase} prompt generated successfully")
                else:
                    print(f"❌ {phase} prompt seems too short")
                    return False

            except Exception as e:
                print(f"❌ Error with {phase} prompt: {e}")
                return False

        print("✅ All prompt phases working correctly")
        return True

    except Exception as e:
        print(f"❌ Dispatcher error: {e}")
        return False

def test_error_handling():
    """Test error handling in the utilities"""
    print("\n🔄 Testing error handling...")

    try:
        from utils.prompts import ImmigrationFormPrompts

        # Test invalid phase
        try:
            ImmigrationFormPrompts.get_prompt_by_phase("invalid_phase")
            print("❌ Should have raised error for invalid phase")
            return False
        except ValueError as e:
            if "Unknown phase" in str(e):
                print("✅ Invalid phase error handling working")
            else:
                print(f"❌ Unexpected error message: {e}")
                return False

        print("✅ Error handling working correctly")
        return True

    except Exception as e:
        print(f"❌ Error handling test failed: {e}")
        return False

def print_summary(tests_passed, total_tests):
    """Print test summary"""
    print("\n" + "="*50)
    print("📊 TEST SUMMARY")
    print("="*50)

    if tests_passed == total_tests:
        print(f"🎉 ALL TESTS PASSED! ({tests_passed}/{total_tests})")
        print("\n✅ Your prompt utilities are ready to use!")
        print("\nNext steps:")
        print("1. Update your .env file with API keys")
        print("2. Run the Supabase database schema")
        print("3. Update your main translator class")
        print("4. Test with your existing backend")
    else:
        print(f"❌ {tests_passed}/{total_tests} tests passed")
        print("\n🔧 Fix the failing tests before proceeding")
        print("Check that:")
        print("- All files are in the correct location")
        print("- No syntax errors in the utility files")
        print("- You're running from the correct directory")

    print("\n📁 Expected file structure:")
    print("your-project/")
    print("├── utils/")
    print("│   ├── __init__.py")
    print("│   ├── prompts.py")
    print("│   ├── prompt_config.py")
    print("│   └── prompt_manager.py")
    print("├── test_utilities.py")
    print("└── ... (your other files)")

def main():
    """Run all utility tests"""
    print("🚀 Immigration Form Translation - Utilities Test")
    print("="*50)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Python version: {sys.version}")
    print(f"Current directory: {os.getcwd()}")
    print("="*50)

    tests = [
        ("Import Test", test_imports),
        ("Prompt Generation", test_prompt_generation),
        ("Configuration", test_configuration),
        ("Prompt Manager", test_prompt_manager),
        ("Dispatcher", test_dispatcher),
        ("Error Handling", test_error_handling)
    ]

    tests_passed = 0
    total_tests = len(tests)

    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if test_func():
                tests_passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} CRASHED: {e}")

    print_summary(tests_passed, total_tests)

if __name__ == "__main__":
    main()