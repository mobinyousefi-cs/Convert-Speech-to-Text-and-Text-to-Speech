#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Basic smoke tests that do not trigger audio hardware/network.
"""
from speech_text_converter import __version__, speak_text


def test_version_semver_like():
    assert isinstance(__version__, str)
    assert __version__.count(".") >= 1


def test_tts_noop_on_empty_text():
    # Should not raise for blank text (and should be a no-op)
    speak_text("")
    speak_text("   ")
