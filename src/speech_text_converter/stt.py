#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=========================================================================================================
Project: Speech–Text Converter (Speech Recognition + Text-to-Speech)
File: stt.py
Author: Mobin Yousefi (GitHub: https://github.com/mobinyousefi-cs)
Created: 2025-10-06
Updated: 2025-10-06
License: MIT License (see LICENSE file for details)
=========================================================================================================

Description:
Speech-to-Text utilities using SpeechRecognition. Recognizes mic input via
Google Web Speech API. Requires internet and PyAudio for microphone access.

Usage:
from speech_text_converter.stt import stt_from_mic
text = stt_from_mic(language="en-US")
print(text)

Notes:
- You may need to install PyAudio wheels on Windows.
- `language` should be a BCP-47 code (e.g., en-US, fa-IR).
"""
from __future__ import annotations

import speech_recognition as sr


def stt_from_mic(
    language: str = "en-US",
    timeout: float | None = 5.0,
    phrase_time_limit: float | None = 5.0,
) -> str:
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
    # Use Google Web Speech API
    return r.recognize_google(audio, language=language)
