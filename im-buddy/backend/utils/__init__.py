# utils/__init__.py
"""
Immigration Form Translation Utilities Package

This package contains prompt management and configuration utilities
for the Llama 4-powered immigration form translation system.
"""

from .prompts import ImmigrationFormPrompts, PromptManager
from .prompt_config import PromptConfig

__version__ = "1.0.0"
__author__ = "Immigration Form Translation System"

__all__ = [
    "ImmigrationFormPrompts",
    "PromptManager",
    "PromptConfig"
]