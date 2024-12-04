# Automated Unicorn

## Quickstart

As a *root* user:

```bash
# Prerequisites
apt-get install podman

# Run the privileged container
podman run --replace --name automated-unicorn --privileged --device /dev/snd -p 5000:5000 -d -v /home/<YOUR_USER>/MP3:/app/MP3 quay.io/jwerak/automated-unicorn

# Test
curl localhost:5000/unicorn/audio -X POST -H "Content-Type: application/json" -d "{}"
```

## Setup

### Install

```bash
apt-get update && apt-get install -y python3-rpi.gpio mpg321

pip install -r requirements.txt
```

### Run the app

```bash
export PATH_AUDIO=/home/UNI-pi/kiosk/MP3
python3 app.py
```

### Create SystemD unit

- Create service file: `/etc/systemd/system/unicorn.service`, see below
- reload systemd: `systemctl daemon-reload`
- enable unit: `systemctl enable unicorn.service`
- start unit: `systemctl start unicorn.service`

```ini
[Unit]
Description=Automated Unicorn
After=network.target

[Service]
Environment="PATH_AUDIO=/home/UNI-pi/kiosk/MP3"
Environment="CONTROLLER_USERNAME=admin"
Environment="CONTROLLER_PASSWORD=password"

# Absolute path to the Python interpreter
ExecStart=/usr/bin/python3 /home/UNI-pi/automated_unicorn-master/app.py

# Restart policy
Restart=always
RestartSec=2

# Standard output and error logs (optional)
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

## Container setup

### Build Container

```bash
podman build -t quay.io/jwerak/automated-unicorn .
```

### Run Container

As `root` user run

```bash
podman run --replace --name automated-unicorn -e PATH_AUDIO=/MP3 --privileged --device /dev/snd -p 5000:5000 -d -v /home/UNI-pi/kiosk/MP3:/MP3 quay.io/jwerak/automated-unicorn
```

## Test

### Test the Color GET Endpoint

To retrieve the current color:

```bash
curl -X GET http://localhost:5000/unicorn/color
```

Expected Response:

```json
{
  "color": "current_color"
}
```

### Test the Color POST Endpoint

To set a new color (replace <color_value> with your desired color, like "blue"):

```bash
curl -X POST http://localhost:5000/unicorn/color -H "Content-Type: application/json" -d '{"color": "<color_value>"}'
```

Expected Response:

```json
{
  "status": "success",
  "color": "<color_value>"
}
```

### Test the Audio POST Endpoint

To play an audio file (replace /path/to/audio.mp3 with the path to your MP3 file):

```bash
curl -X POST http://localhost:5000/unicorn/audio -H "Content-Type: application/json" -d '{"audio_file": "/path/to/audio.mp3"}'

# e.g.
curl -X POST http://192.168.1.195:5000/unicorn/audio -H "Content-Type: application/json" -d '{"audio_file": "Cantina.mp3"}'
```

Expected Response:

```json
{
  "status": "playing",
  "audio_file": "/path/to/audio.mp3"
}
```

### GET /unicorn/audio: Check the last played audio

```bash
curl -X GET http://localhost:5000/unicorn/audio
```

Possible Responses:

If an audio file was played:

```json
{
  "status": "last played",
  "audio_file": "/path/to/last_played_audio.mp3"
}
```

If no audio has been played:

```json
{
  "status": "no audio has been played yet"
}
```

## Notes

Tested on rpi 4b 64bit

```txt
PRETTY_NAME="Debian GNU/Linux 11 (bullseye)"
NAME="Debian GNU/Linux"
VERSION_ID="11"
VERSION="11 (bullseye)"
VERSION_CODENAME=bullseye
ID=debian
```
