# 🖼️ Image Renamer with EXIF + Voice Input

This is a Python tool for interactively renaming photos based on:
- EXIF photo date
- GPS coordinates (converted to city name)
- A spoken description (via microphone)

Final filename format:
YYYY MM DD City Description.jpg

---

## 🔧 Installation

### 1. Clone this repo and enter the project folder

git clone https://your-repo-url
cd image-renamer

### 2. (Optional) Create a virtual environment

python3 -m venv venv
source venv/bin/activate

### 3. Install dependencies

pip install -r requirements.txt

If you're on Linux and get errors with `sounddevice`, install portaudio:

sudo apt install portaudio19-dev python3-pyaudio


## 🔊 Vosk Model (for voice input)

Download a small English speech model:

wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
unzip vosk-model-small-en-us-0.15.zip
mv vosk-model-small-en-us-0.15 model

Make sure the `model/` folder sits next to your Python files.

---

## 📁 Folder Structure

image-renamer/
├── main.py
├── image_viewer.py
├── exif_reader.py
├── geolocator.py
├── voice_input.py
├── renamer.py
├── requirements.txt
├── model/                  # Vosk model folder
└── photos/                 # Place your images here

---

## 🚀 Running the App

python main.py

- Use ← and → arrow keys to navigate images.
- Each image triggers voice input.
- When satisfied, turn off test mode in `main.py` to apply real renaming.

---

## ✅ Notes

- Supported formats: .jpg, .jpeg, .png
- Falls back to file mod time if no EXIF date
- Falls back to empty city if no GPS

---

## 📌 Future Features

- Undo renames
- Batch mode
- Auto-skip already processed files