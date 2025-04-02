from PIL import Image
import piexif
from datetime import datetime
from pathlib import Path

def get_image_date(image_path: Path) -> datetime:
    try:
        exif_dict = piexif.load(str(image_path))
        date_str = exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal].decode()
        return datetime.strptime(date_str, "%Y:%m:%d %H:%M:%S")
    except Exception:
        # Fallback to file modification time
        return datetime.fromtimestamp(image_path.stat().st_mtime)

def get_gps_coordinates(image_path: Path):
    try:
        exif_dict = piexif.load(str(image_path))
        gps = exif_dict.get("GPS")
        if not gps:
            return None

        def to_degrees(value):
            d, m, s = value
            return d[0]/d[1] + m[0]/m[1]/60 + s[0]/s[1]/3600

        lat = to_degrees(gps[piexif.GPSIFD.GPSLatitude])
        lon = to_degrees(gps[piexif.GPSIFD.GPSLongitude])

        if gps[piexif.GPSIFD.GPSLatitudeRef] == b'S':
            lat = -lat
        if gps[piexif.GPSIFD.GPSLongitudeRef] == b'W':
            lon = -lon

        return (lat, lon)
    except Exception:
        return None

# For testing
if __name__ == "__main__":
    test_path = Path("./photos/IMG_7776.jpg")
    print("Date:", get_image_date(test_path))
    print("GPS:", get_gps_coordinates(test_path))
