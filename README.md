# Neura – AI-Powered Voice Assistant 🔊🤖

Neura is a Python-based AI voice assistant capable of understanding voice commands, performing tasks like opening apps, playing YouTube videos, sending WhatsApp messages, and more — all with a friendly voice interface.

## 🚀 Features
- Hotword detection ("Hey Neura")
- Speech-to-text and text-to-speech interaction
- Opens apps and websites
- YouTube search and play
- WhatsApp messaging and calling
- GUI integration with Eel

## 🛠️ Tech Stack

- **Python** – Core logic and voice engine
- **Eel** – Python + Web GUI integration
- **HTML, CSS, JavaScript** – Frontend interface for Neura
- **SpeechRecognition**, **PyWhatKit**, **Porcupine** – Voice and automation features
- **SQLite** – For storing custom app commands

## 📁 Project Structure

```
your_folder/
├── engine/
├── templates/
├── static/
├── main.py
├── neura.db
└── README.md
```

## 🧪 How to Run
```bash
pip install -r requirements.txt
python main.py
