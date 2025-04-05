import os
from pathlib import Path

def sanitize_text(text: str) -> str:
    """Sanitize text by removing invalid characters for filenames."""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        text = text.replace(char, "")
    return text.strip()

def build_new_filename(date, prefix, city, postfix, description, original_ext):
    """Build a new filename based on the provided components."""
    date_str = date.strftime("%Y %m %d") if date else ""  # Handle None for date
    prefix_part = sanitize_text(prefix) if prefix else ""  # Use the provided prefix
    city_part = sanitize_text(city) if city else ""
    postfix_part = sanitize_text(postfix) if postfix else ""  # Sanitize the postfix
    desc_part = sanitize_text(description) if description else ""
    parts = [part for part in [date_str, prefix_part, city_part, postfix_part, desc_part] if part]  # Include postfix
    return " ".join(parts) + original_ext

def rename_image(image_path: Path, date, prefix: str, city: str, postfix: str, description: str, test_mode=False):
    """Rename the image file based on the new filename."""
    original_ext = image_path.suffix.lower()
    new_name = build_new_filename(date, prefix, city, postfix, description, original_ext)
    new_path = image_path.parent / new_name

    if test_mode:
        print(f"[TEST MODE] Would rename: {image_path} -> {new_path}")
    else:
        print(f"Renaming: {image_path} -> {new_path}")
        os.rename(image_path, new_path)

# For testing
if __name__ == "__main__":
    from datetime import datetime

    test_path = Path("./photos/IMG_7776.jpg")
    test_date = datetime(2023, 9, 15)  # Example date
    test_prefix = "Vacation"
    test_city = "New York"
    test_postfix = "Evening"
    test_description = "Central Park"
    test_ext = ".jpg"

    print("New Filename:", build_new_filename(test_date, test_prefix, test_city, test_postfix, test_description, test_ext))
