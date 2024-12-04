from flask import Flask, request, jsonify
import os
import RPi.GPIO as GPIO
import subprocess
import threading
import requests
from requests.auth import HTTPBasicAuth

# Initialize Flask app
app = Flask(__name__)

# Preset variables
PATH_AUDIO = os.getenv("PATH_AUDIO", "/home/UNI-pi/kiosk/MP3/")

# Store the last played audio file for GET requests
last_audio_file = ""

# Store the current unicorn color
current_color = None

# Credentials for external API
CONTROLLER_USERNAME = os.getenv("CONTROLLER_USERNAME", "admin")
CONTROLLER_PASSWORD = os.getenv("CONTROLLER_PASSWORD", "default_pass")

LAUNCH_URL = "https://caap-automates-prague.cjung.ansible-labs.de/api/controller/v2/job_templates/Unicorn%2FFixColor++Default/launch/"


# GPIO setup
def initialize_gpio():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(17, GPIO.OUT)
    GPIO.setup(27, GPIO.OUT)
    GPIO.setup(22, GPIO.OUT)
    GPIO.setup(4, GPIO.OUT)

    GPIO.output(17, GPIO.HIGH)
    GPIO.output(27, GPIO.HIGH)
    GPIO.output(22, GPIO.HIGH)
    GPIO.output(4, GPIO.HIGH)
    print("GPIO initialized")


# Initialize GPIO on startup
initialize_gpio()


def stop_color():
    pin_numbers = [17, 27, 22]

    for pin_number in pin_numbers:
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin_number, GPIO.OUT)
        GPIO.output(pin_number, GPIO.HIGH)


# Set color
def change_color(color):
    stop_color()
    pin_number = 17

    if color == "red":
        pin_number = 17
    elif color == "green":
        pin_number = 27
    elif color == "blue":
        pin_number = 22

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin_number, GPIO.OUT)
    GPIO.output(pin_number, GPIO.LOW)


# Function to play audio asynchronously
def play_audio(file_path):
    global last_audio_file
    last_audio_file = file_path  # Save the file being played
    subprocess.run(
        ["mpg321", "-q", "-B", file_path],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


# Endpoint to get or set unicorn color
@app.route("/unicorn/color", methods=["GET", "POST"])
def unicorn_color():
    global current_color
    if request.method == "GET":
        # If current_color is None, it means it hasn't been set yet.
        # Adjust logic if you want a default color.
        color = current_color if current_color else "unknown"
        return jsonify({"color": color}), 200
    elif request.method == "POST":
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400

        new_color = data.get("color")
        if not new_color:
            return jsonify({"error": "No color provided"}), 400

        # Check if the new color is different from the current one
        if new_color != current_color:
            print(f"Setting unicorn color to {new_color}")
            change_color(new_color)
            current_color = new_color

            # Post to external endpoint if color changed
            try:
                response = requests.post(
                    LAUNCH_URL,
                    auth=HTTPBasicAuth(CONTROLLER_USERNAME, CONTROLLER_PASSWORD),
                    # Adjust if the API requires a specific payload
                )
                if response.status_code not in (200, 201, 202):
                    print(
                        f"Failed to launch job template: {response.status_code}, {response.text}"
                    )
                else:
                    print("Successfully launched job template.")
            except Exception as e:
                print(f"Error posting to launch endpoint: {e}")

            return jsonify({"status": "success", "color": new_color}), 200
        else:
            # Color is the same; do nothing special
            return jsonify({"status": "no change", "color": current_color}), 200


# Endpoint to handle unicorn audio via POST
@app.route("/unicorn/audio", methods=["GET", "POST"])
def unicorn_audio():
    global last_audio_file
    if request.method == "GET":
        # Respond with the last played audio file or a default message
        if last_audio_file:
            return (
                jsonify({"status": "last played", "audio_file": last_audio_file}),
                200,
            )
        else:
            return jsonify({"status": "no audio has been played yet"}), 200

    elif request.method == "POST":
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400

        audio_file = data.get("audio_file", "")
        if not audio_file:
            return jsonify({"error": "No audio file provided"}), 400

        audio_path = f"{PATH_AUDIO}/{audio_file}"

        threading.Thread(target=play_audio, args=(audio_path,), daemon=True).start()
        return jsonify({"status": "playing", "audio_file": audio_file}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
