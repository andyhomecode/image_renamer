# 🖼️ Image Renamer with EXIF
# Andy Maxwell 
# 0.1 4/4/2025


This is a Python tool for renaming and deleting large batches of photos in a folder.

The goal was to make something that would be fast to use just with the keyboard.

Image files are examined to get the 

- EXIF photo date
- GPS coordinates (converted to city name)

Then the user can edits them and enters: 
- an optional prefix to group photos (e.g. "Beach Day), and
- a typed description of the one photo (e.g. "Andy playing in the surf")

Final filename format for ease of searching and sorting photos:

`YYYY MM DD Prefix City Description.jpg`

e.g.

`2025 06 20 Beach Day Rehoboth Andy Playing in the surf.jpg`

files can be 'deleted', which moves them into a 'deleted' subfolder

The program creates a .bat or .sh script file in the photo directory to make the changes rather than doing the changes itself.  This makes testing easy and allows you to review the changes before they happen.

---

## 🔧 Installation

### 1. Clone this repo and enter the project folder

```bash
git clone https://github.com/andyhomecode/image_renamer
cd image-renamer
```

### 2. (Optional) Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
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
├── voice_input.py # empty, functionality deleted because it was lame
├── requirements.txt
├── README.md
└── photos/        # Place test images here
```

---

## 🚀 Running the App

```bash
python main.py <path_to_photos_folder>
```

For example:

```bash
python main.py ./photos
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
  - `Shift + F2`: Clear the prefix (global and current image).
  - `F3`: Include/Exclude the location in the filename.
  - `Shift + F3`: Reload the geolocation from the file and update the location field.
  - `F4`: Show/Hide the overlay to view the image without distractions.
- **Final Name**:
  - The overlay dynamically updates to show the final filename based on the current inputs and toggles.
- **Delete**:
  - Press `Delete` to mark the file for deletion by moving into a 'deleted' folder and move to the next image.

---

## ✅ Notes

- Supported formats: `.jpg`, `.jpeg`, `.png`
- Falls back to file modification time if no EXIF date is available.
- Falls back to an empty city if no GPS data is available.
- Batch files are generated for renaming and moving files:
  - On **Windows**: A `.bat` file is created.
  - On **Linux/Mac**: A `.sh` file is created.

---

## 📌 Future Features

- None. It emerged perfectly like Athena from Zeus's head.

---

## 📌 TODOs

- [ ] also none.

---

## 🤖 This was mostly vibe coded using ChatGPT initially, then VS Code w/Copilot once I split it up into multiple files.
