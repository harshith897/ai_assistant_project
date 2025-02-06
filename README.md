# AI Assistant Prototype

This project contains a simple prototype for a Python-based AI assistant that includes:

- **Flask Backend Server:**  
  Manages reminders and receives commands.

- **Desktop Agent:**  
  Uses SpeechRecognition, pyttsx3, and spaCy to listen for voice commands, analyze intents, and execute actions.

- **Mobile App (Kivy):**  
  A simple mobile interface for adding reminders that communicates with the Flask server.

## Installation and Setup

1. **Clone the repository and navigate into the project folder.**

2. **Set up a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
