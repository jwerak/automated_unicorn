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
python3 app.py
```

## Container setup

### Build Container

```bash
podman build -t unicorn-app .
```

### Run Container

As `root` user run

```bash
podman run -d -p 5000:5000 --name unicorn-container --privileged unicorn-app
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
