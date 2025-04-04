# 🖼️ Image Renamer with EXIF

This is a Python tool for interactively renaming photos based on:
- EXIF photo date
- GPS coordinates (converted to city name)
- A typed description

Final filename format:
YYYY MM DD Prefix City Description.jpg

---

## 🔧 Installation

### 1. Clone this repo and enter the project folder

```bash
git clone https://your-repo-url
cd image-renamer
```

### 2. (Optional) Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 📁 Folder Structure

```
image-renamer/
├── main.py
├── image_viewer.py
├── exif_reader.py
├── geolocator.py
├── renamer.py
├── requirements.txt
└── photos/                 # Place your images here
```

---

## 🚀 Running the App

```bash
python main.py
```

### Overlay Controls:
- **Arrow Keys**:
  - `←` and `→`: Navigate between images.
  - `↑` and `↓`: Switch between editable fields (Date, Prefix, Location, Description).
- **Editing Fields**:
  - Type to edit the selected field.
  - Press `Backspace` to delete characters.
  - Press `Enter` to confirm the current field or finalize the rename.
- **Toggles**:
  - `F1`: Include/Exclude the date in the filename.
  - `F2`: Include/Exclude the prefix in the filename.
  - `F3`: Include/Exclude the location in the filename.
  - `Shift + F3`: Reload the geolocation from the file and update the location field.
  - `F4`: Show/Hide the overlay to view the image without distractions.
- **Final Name**:
  - The overlay dynamically updates to show the final filename based on the current inputs and toggles.

---

## ✅ Notes

- Supported formats: `.jpg`, `.jpeg`, `.png`
- Falls back to file modification time if no EXIF date is available.
- Falls back to an empty city if no GPS data is available.

---

## 📌 Future Features

- Undo renames.
- Batch mode for processing multiple images at once.
- Auto-skip already processed files.
- Pre-process image categorization using AI to speed up tagging.

---

## 📌 TODOs

- [ ] Update the EXIF metadata with the edited date or other fields (e.g., location, description).
- [ ] Add undo functionality for renames.
- [ ] Implement batch mode for processing multiple images at once.
- [ ] Pre-process image categorization using AI to speed up tagging.
