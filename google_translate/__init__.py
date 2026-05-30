"""
Google Translate API Package
A Python package for interacting with Google Translate services.
"""

__version__ = "0.2.0"
__author__ = "etrnkz"

from .text import translate_text
from .image import translate_image
from .docs import translate_document
from .voice import translate_voice
from .websites import translate_website

__all__ = [
    'translate_text',
    'translate_image',
    'translate_document',
    'translate_voice',
    'translate_website'
]
