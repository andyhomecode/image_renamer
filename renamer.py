import os
from pathlib import Path

def sanitize_text(text: str) -> str:
    """Sanitize text by removing invalid characters for filenames."""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        text = text.replace(char, "")
    return text.strip()

def build_new_filename(date, prefix, city, description, original_ext):
    """Build a new filename based on the provided components."""
    date_str = date.strftime("%Y %m %d") if date else ""  # Handle None for date
    prefix_part = sanitize_text(prefix) if prefix else ""  # Use the provided prefix
    city_part = sanitize_text(city) if city else ""
    desc_part = sanitize_text(description) if description else ""
    parts = [part for part in [date_str, prefix_part, city_part, desc_part] if part]  # Filter out empty parts
    return " ".join(parts) + original_ext

def rename_image(image_path: Path, date, prefix: str, city: str, description: str, test_mode=False):
    """Rename the image file based on the new filename."""
    original_ext = image_path.suffix.lower()
    new_name = build_new_filename(date, prefix, city, description, original_ext)
    new_path = image_path.parent / new_name

    if test_mode:
        print(f"[TEST MODE] Would rename: {image_path} -> {new_path}")
    else:
        print(f"Renaming: {image_path} -> {new_path}")
        os.rename(image_path, new_path)

# For testing
if __name__ == "__main__":
    test_path = Path("./photos/IMG_7776.jpg")
    print("New Filename:", build_new_filename(None, "Prefix", "New York", "My Description", ".jpg"))
