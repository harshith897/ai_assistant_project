# server.py
from flask import Flask, request, jsonify
app = Flask(__name__)

# In-memory storage for reminders (for prototype purposes)
reminders = []

@app.route('/add_reminder', methods=['POST'])
def add_reminder():
    data = request.get_json()
    reminder = data.get("reminder")
    if reminder:
        reminders.append(reminder)
        return jsonify({"status": "success", "reminders": reminders})
    return jsonify({"status": "error", "message": "No reminder provided"}), 400

@app.route('/get_reminders', methods=['GET'])
def get_reminders():
    return jsonify({"reminders": reminders})

@app.route('/command', methods=['POST'])
def command():
    data = request.get_json()
    # For this prototype, simply echo back the command.
    command_text = data.get("command")
    print(f"Received command: {command_text}")
    # In a more advanced version, you would trigger actions here.
    return jsonify({"status": "success", "message": f"Command '{command_text}' received."})

if __name__ == '__main__':
    # Run on port 5000, accessible to your devices on the same network.
    app.run(host="0.0.0.0", port=5000)
