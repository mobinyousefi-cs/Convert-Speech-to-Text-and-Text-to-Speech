#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=========================================================================================================
Project: Speech–Text Converter (Speech Recognition + Text-to-Speech)
File: gui.py
Author: Mobin Yousefi (GitHub: https://github.com/mobinyousefi-cs)
Created: 2025-10-06
Updated: 2025-10-06
License: MIT License (see LICENSE file for details)
=========================================================================================================

Description:
Tkinter GUI that:
- Records and transcribes microphone audio to text (STT).
- Speaks entered text aloud (TTS).

Usage:
python -m speech_text_converter --gui

Notes:
- STT uses SpeechRecognition (needs PyAudio) + Google API (internet).
- TTS uses gTTS + playsound (internet).
"""
from __future__ import annotations

import threading
import tkinter as tk
from tkinter import ttk, messagebox

from .stt import stt_from_mic
from .tts import speak_text

LANG_CHOICES_STT = [
    ("English (US)", "en-US"),
    ("English (UK)", "en-GB"),
    ("Persian (Iran)", "fa-IR"),
    ("French", "fr-FR"),
    ("German", "de-DE"),
    ("Arabic", "ar-SA"),
    ("Spanish", "es-ES"),
    ("Hindi", "hi-IN"),
]

LANG_CHOICES_TTS = [
    ("English", "en"),
    ("Persian", "fa"),
    ("French", "fr"),
    ("German", "de"),
    ("Arabic", "ar"),
    ("Spanish", "es"),
    ("Hindi", "hi"),
]


def _async_call(fn, on_error=None):
    th = threading.Thread(target=fn, daemon=True)
    th.start()
    return th


def run_gui() -> None:
    root = tk.Tk()
    root.title("Speech ↔ Text Converter — Mobin Yousefi")
    root.geometry("720x520")

    # Styles
    style = ttk.Style()
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    # Frames
    container = ttk.Frame(root, padding=12)
    container.pack(fill=tk.BOTH, expand=True)

    # --- STT Section ---
    stt_frame = ttk.LabelFrame(container, text="Speech → Text (Microphone)", padding=12)
    stt_frame.pack(fill=tk.X, expand=False)

    lang_lbl = ttk.Label(stt_frame, text="Language:")
    lang_lbl.grid(row=0, column=0, sticky=tk.W, padx=(0, 8), pady=4)

    stt_lang_var = tk.StringVar(value="en-US")
    stt_lang_combo = ttk.Combobox(
        stt_frame,
        textvariable=stt_lang_var,
        values=[code for _, code in LANG_CHOICES_STT],
        state="readonly",
        width=12,
    )
    stt_lang_combo.grid(row=0, column=1, sticky=tk.W, pady=4)

    stt_btn = ttk.Button(stt_frame, text="Start Listening", width=18)
    stt_btn.grid(row=0, column=2, padx=8, pady=4)

    stt_output = tk.Text(stt_frame, height=6, wrap=tk.WORD)
    stt_output.grid(row=1, column=0, columnspan=3, sticky="nsew", pady=(8, 0))
    stt_frame.grid_columnconfigure(2, weight=1)
    stt_frame.grid_rowconfigure(1, weight=1)

    # --- TTS Section ---
    tts_frame = ttk.LabelFrame(container, text="Text → Speech (gTTS)", padding=12)
    tts_frame.pack(fill=tk.BOTH, expand=True, pady=(12, 0))

    tts_lang_lbl = ttk.Label(tts_frame, text="Language:")
    tts_lang_lbl.grid(row=0, column=0, sticky=tk.W, padx=(0, 8), pady=4)

    tts_lang_var = tk.StringVar(value="en")
    tts_lang_combo = ttk.Combobox(
        tts_frame,
        textvariable=tts_lang_var,
        values=[code for _, code in LANG_CHOICES_TTS],
        state="readonly",
        width=12,
    )
    tts_lang_combo.grid(row=0, column=1, sticky=tk.W, pady=4)

    slow_var = tk.BooleanVar(value=False)
    slow_chk = ttk.Checkbutton(tts_frame, text="Slow", variable=slow_var)
    slow_chk.grid(row=0, column=2, sticky=tk.W, padx=8, pady=4)

    tts_text = tk.Text(tts_frame, height=8, wrap=tk.WORD)
    tts_text.grid(row=1, column=0, columnspan=3, sticky="nsew", pady=(8, 0))
    tts_frame.grid_columnconfigure(2, weight=1)
    tts_frame.grid_rowconfigure(1, weight=1)

    tts_btn = ttk.Button(tts_frame, text="Speak Text", width=18)
    tts_btn.grid(row=2, column=0, sticky=tk.W, pady=8)

    # Status bar
    status_var = tk.StringVar(value="Ready.")
    status = ttk.Label(root, textvariable=status_var, relief=tk.SUNKEN, anchor=tk.W)
    status.pack(fill=tk.X, side=tk.BOTTOM)

    # --- Event handlers ---
    def do_stt():
        stt_btn.config(state=tk.DISABLED)
        status_var.set("Listening… speak now.")
        stt_output.delete("1.0", tk.END)

        def worker():
            try:
                text = stt_from_mic(language=stt_lang_var.get(), timeout=5, phrase_time_limit=5)
                root.after(0, lambda: stt_output.insert(tk.END, text if text else ""))
                root.after(0, lambda: status_var.set("Transcription complete."))
            except Exception as exc:  # noqa: BLE001
                root.after(0, lambda: messagebox.showerror("STT Error", str(exc)))
                root.after(0, lambda: status_var.set("STT failed."))
            finally:
                root.after(0, lambda: stt_btn.config(state=tk.NORMAL))

        _async_call(worker)

    def do_tts():
        txt = tts_text.get("1.0", tk.END).strip()
        if not txt:
            messagebox.showinfo("Empty Text", "Please type some text to speak.")
            return

        tts_btn.config(state=tk.DISABLED)
        status_var.set("Generating speech…")

        def worker():
            try:
                speak_text(txt, lang=tts_lang_var.get(), slow=slow_var.get())
                root.after(0, lambda: status_var.set("Playback done."))
            except Exception as exc:  # noqa: BLE001
                root.after(0, lambda: messagebox.showerror("TTS Error", str(exc)))
                root.after(0, lambda: status_var.set("TTS failed."))
            finally:
                root.after(0, lambda: tts_btn.config(state=tk.NORMAL))

        _async_call(worker)

    stt_btn.config(command=do_stt)
    tts_btn.config(command=do_tts)

    root.mainloop()
