#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=========================================================================================================
Project: Speech–Text Converter (Speech Recognition + Text-to-Speech)
File: tts.py
Author: Mobin Yousefi (GitHub: https://github.com/mobinyousefi-cs)
Created: 2025-10-06
Updated: 2025-10-06
License: MIT License (see LICENSE file for details)
=========================================================================================================

Description:
Text-to-Speech utilities using gTTS + playsound.

Usage:
from speech_text_converter.tts import speak_text
speak_text("Hello!", lang="en")

Notes:
- gTTS requires internet. It saves an MP3 and plays it with playsound.
"""
from __future__ import annotations

import os
import tempfile
from gtts import gTTS
from playsound import playsound


def speak_text(text: str, lang: str = "en", slow: bool = False) -> None:
    text = (text or "").strip()
    if not text:
        return
    tts = gTTS(text=text, lang=lang, slow=slow)
    # Temporary MP3 file
    with tempfile.NamedTemporaryFile(prefix="gtts_", suffix=".mp3", delete=False) as fp:
        path = fp.name
    try:
        tts.save(path)
        playsound(path)
    finally:
        try:
            os.remove(path)
        except OSError:
            pass
