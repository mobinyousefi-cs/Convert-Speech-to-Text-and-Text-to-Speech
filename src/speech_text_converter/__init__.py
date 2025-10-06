#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=========================================================================================================
Project: Speech–Text Converter (Speech Recognition + Text-to-Speech)
File: __init__.py
Author: Mobin Yousefi (GitHub: https://github.com/mobinyousefi-cs)
Created: 2025-10-06
Updated: 2025-10-06
License: MIT License (see LICENSE file for details)
=========================================================================================================

Description:
Package initializer exposing a simple public API.
"""

__all__ = ["run_gui", "cli_main", "stt_from_mic", "speak_text"]
__version__ = "0.1.0"

from .gui import run_gui  # noqa: E402
from .main import cli_main  # noqa: E402
from .stt import stt_from_mic  # noqa: E402
from .tts import speak_text  # noqa: E402
