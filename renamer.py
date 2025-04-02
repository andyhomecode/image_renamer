import os
from pathlib import Path

def sanitize_text(text: str) -> str:
    # Remove or replace invalid characters for filenames
    return ''.join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in text).strip()

def build_new_filename(date, city, description, original_ext):
    date_str = date.strftime("%Y %m %d")
    city_part = sanitize_text(city)
    desc_part = sanitize_text(description)
    parts = [date_str]
    if city_part:
        parts.append(city_part)
    if desc_part:
        parts.append(desc_part)
    return ' '.join(parts) + original_ext

def rename_image(image_path: Path, date, city: str, description: str, test_mode=False):
    new_name = build_new_filename(date, city, description, image_path.suffix.lower())
    new_path = image_path.with_name(new_name)
    if test_mode:
        print(f"[TEST MODE] Would rename: {image_path.name} -> {new_path.name}")
    else:
        if new_path.exists():
            print(f"File already exists: {new_path.name}, skipping rename.")
        else:
            image_path.rename(new_path)
            print(f"Renamed to: {new_path.name}")

# For testing
if __name__ == "__main__":
    from datetime import datetime
    dummy_path = Path("./photos/test_image.jpg")
    rename_image(dummy_path, datetime(2023, 9, 17), "Tokyo", "Street Festival", test_mode=True)