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
├── image_viewer.py  # worked straight from GPT
├── exif_reader.py  # worked straight from GPT
├── geolocator.py    # worked straight from GPT
├── voice_input.py   # worked straight from GPT
├── renamer.py		# worked straight from GPT 100% functional!!!
├── requirements.txt   # worked straight from GPT
├── model/                  # Vosk model folder
└── photos/                 # Place your images here

---

## 🚀 Running the App

python main.py

- Use ← and → arrow keys to navigate between images.
- For each image, a floating overlay window will appear.
- You can type a description, and optionally use a persistent prefix.
- Press `L` to toggle including/excluding the location in the filename.
- Press `P` to toggle using a persistent prefix.
- Press `Enter` to confirm and rename the image (or preview if in test mode).
- When satisfied, turn off `test_mode` in `main.py` to apply real renaming.

---

## ✅ Notes

- Supported formats: .jpg, .jpeg, .png
- Falls back to file mod time if no EXIF date
- Falls back to empty city if no GPS

- ## 🎮 Keyboard Controls

| Key     | Action                          |
|---------|---------------------------------|
| ← / →   | Move to previous/next image     |
| `L`     | Toggle location ON/OFF          |
| `P`     | Toggle prefix ON/OFF            |
| Typing  | Enter image description         |
| `Enter` | Confirm and rename image        |


---

## 📌 Future Features

- Undo renames
- Batch mode
- Auto-skip already processed files
- ANDY: Consider pre-processing date and location into .csv files to speed categorization.
- ANDY: consider pre-processing image categorization using imagenet or LLM to identify people, major things, to speed categorization
