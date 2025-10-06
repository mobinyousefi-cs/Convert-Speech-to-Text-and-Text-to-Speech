# Speech–Text Converter (Tkinter GUI + CLI)

A polished Python project that converts **speech → text** (microphone, SpeechRecognition) and **text → speech** (gTTS). Includes a modern Tkinter GUI and a convenient CLI.

## ✨ Features
- 🎙️ **Speech → Text**: Recognize mic input via Google Web Speech API  
- 🗣️ **Text → Speech**: gTTS with optional slow mode  
- 🪟 **Tkinter GUI**: Simple, responsive UI  
- 🧪 **Tests + CI**: Smoke tests and GitHub Actions  
- 📦 **PEP 621** packaging with `pyproject.toml`

## 📦 Installation
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .
pip install -r requirements.txt
