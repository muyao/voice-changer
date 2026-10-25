# Voice Changer

A simple voice changer with Python

---

## Features

* Configurable with a custom `config.json`.
* Pre-existing voicechangers in `presets/`.

---

## Installation

### Prerequisites

* Python
* BlackHole (Or any ther audio driver)

### Setup Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/muyao/voice-changer.git
   cd voice-changer
   ```
2. **Install requirements:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Give** `start.py` **and** `stop.py` **permissions:**
   ```bash
   chmod +x start.py stop.py
   ```

---

## Usage

* **Starting:**
   ```bash
   ./start.py &
   ```

* **Stopping:**
   ```bash
   ./stop.py
   ```

* **Using preset:**
   ```bash
   ./start.py [preset_path] &
   ```

* **Configuring:**
   ```json
   {
     "version": 2,
     "mic_name": "", // The device name of your physical microphone
     "virtual_name": "BlackHole 2ch", // The name of your virtual microphone
     "config": {
       "50-300": ["2000-2250", 1.5], // Frequencies 50-300hz in the output are 1.5 times loudness frequencies 2000-2250hz in the input. The rest is mute
     }
   }
   ```

---

## License

Distributed under the MIT License. See `LICENSE` for more information.
