from flask import Flask, request, jsonify
import RPi.GPIO as GPIO
import subprocess
import threading

# Initialize Flask app
app = Flask(__name__)

# Preset variables
PATH_AUDIO = "/home/UNI-pi/kiosk/MP3"

# Store the last played audio file for GET requests
last_audio_file = None


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


# Function to play audio asynchronously
def play_audio(file_path):
    global last_audio_file
    last_audio_file = file_path  # Save the file being played
    subprocess.run(["mpg321", file_path])


# Endpoint to get or set unicorn color
@app.route("/unicorn/color", methods=["GET", "POST"])
def unicorn_color():
    if request.method == "GET":
        # Retrieve current color (placeholder logic)
        color = "current_color"
        return jsonify({"color": color}), 200
    elif request.method == "POST":
        # Changing color to red only for now
        # data = request.json
        # color = data.get("color")
        color = "red"
        # Set color logic here using GPIO pins
        print(f"Setting unicorn color to {color}")

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(17, GPIO.OUT)
        GPIO.output(17, GPIO.LOW)

        return jsonify({"status": "success", "color": color}), 200


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
        audio_file = data.get("audio_file")
        audio_path = f"{PATH_AUDIO}/{audio_file}"

        threading.Thread(target=play_audio, args=(audio_path,), daemon=True).start()
        return jsonify({"status": "playing", "audio_file": audio_file}), 200


# Graceful GPIO cleanup
@app.before_first_request
def setup():
    initialize_gpio()


@app.teardown_appcontext
def cleanup_gpio(exception):
    GPIO.cleanup()
    print("GPIO cleaned up")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
