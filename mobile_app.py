# mobile_app.py
import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

# Adjust SERVER_URL to match your server's address (use local IP for real devices)
SERVER_URL = "http://127.0.0.1:5000"

class MainWidget(BoxLayout):
    def add_reminder(self):
        reminder = self.ids.reminder_input.text
        if reminder.strip():
            try:
                response = requests.post(f"{SERVER_URL}/add_reminder", json={"reminder": reminder})
                if response.ok:
                    self.ids.status_label.text = "Reminder added successfully."
                    self.ids.reminder_input.text = ""
                else:
                    self.ids.status_label.text = "Failed to add reminder."
            except Exception as e:
                self.ids.status_label.text = f"Error: {e}"
        else:
            self.ids.status_label.text = "Please enter a reminder."

class MyApp(App):
    def build(self):
        return MainWidget()

if __name__ == '__main__':
    MyApp().run()
