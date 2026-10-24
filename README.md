# Voice Changer

A simple voice changer with Python and BlackHole

---

## Features

* Configurable with a custom `config.json`.
* Pre-existing voicechangers in `presets/`.

---

## Installation

### Prerequisites

* Python
* BlackHole

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

---

## License

Distributed under the MIT License. See `LICENSE` for more information.
