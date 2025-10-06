#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=========================================================================================================
Project: Speech–Text Converter (Speech Recognition + Text-to-Speech)
File: main.py
Author: Mobin Yousefi (GitHub: https://github.com/mobinyousefi-cs)
Created: 2025-10-06
Updated: 2025-10-06
License: MIT License (see LICENSE file for details)
=========================================================================================================

Description:
CLI entry-point and dispatcher for running either the Tkinter GUI or
performing quick speech-to-text or text-to-speech actions from the terminal.

Usage:
python -m speech_text_converter --gui
python -m speech_text_converter stt --lang en-US --timeout 5 --phrase-timeout 5
python -m speech_text_converter tts --text "Hello world" --lang en

Notes:
- STT uses SpeechRecognition + Google Web Speech API (internet required).
- TTS uses gTTS (internet required) and plays via playsound.
- On Windows/macOS/Linux, you may need system audio backends installed.
"""
from __future__ import annotations

import argparse
import sys
from .gui import run_gui
from .stt import stt_from_mic
from .tts import speak_text


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="speech-text-converter",
        description="Convert speech to text (mic) and text to speech (gTTS).",
    )
    sub = parser.add_subparsers(dest="command")

    parser.add_argument(
        "--gui",
        action="store_true",
        help="Launch the Tkinter GUI.",
    )

    stt_p = sub.add_parser("stt", help="Transcribe from microphone.")
    stt_p.add_argument("--lang", default="en-US", help="Recognition language (e.g., en-US, fa-IR).")
    stt_p.add_argument("--timeout", type=float, default=5.0, help="Seconds to wait for phrase start.")
    stt_p.add_argument("--phrase-timeout", type=float, default=5.0, help="Seconds of silence to end phrase.")

    tts_p = sub.add_parser("tts", help="Speak text with gTTS.")
    tts_p.add_argument("--text", required=True, help="Text to speak.")
    tts_p.add_argument("--lang", default="en", help="Voice language (gTTS code, e.g., en, fa).")
    tts_p.add_argument("--slow", action="store_true", help="Speak slowly.")

    return parser


def cli_main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.gui:
        run_gui()
        return 0

    if args.command == "stt":
        try:
            transcript = stt_from_mic(
                language=args.lang,
                timeout=args.timeout,
                phrase_time_limit=args.phrase_timeout,
            )
            print(transcript or "")
            return 0
        except Exception as exc:  # noqa: BLE001
            print(f"[ERROR] STT failed: {exc}", file=sys.stderr)
            return 2

    if args.command == "tts":
        try:
            speak_text(args.text, lang=args.lang, slow=args.slow)
            return 0
        except Exception as exc:  # noqa: BLE001
            print(f"[ERROR] TTS failed: {exc}", file=sys.stderr)
            return 3

    # Default: launch GUI if no subcommand and no --gui given
    run_gui()
    return 0


if __name__ == "__main__":
    raise SystemExit(cli_main())
