from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

geolocator = Nominatim(user_agent="image_renamer")

def reverse_geocode(lat: float, lon: float) -> str:
    try:
        location = geolocator.reverse((lat, lon), language='en', timeout=10)
        if location and "address" in location.raw:
            address = location.raw["address"]
            # Prioritize city, then town, then village
            return address.get("city") or address.get("town") or address.get("village") or ""
        return ""
    except GeocoderTimedOut:
        return reverse_geocode(lat, lon)  # Retry once
    except Exception:
        return ""

# For testing
if __name__ == "__main__":
    lat, lon = 35.6895, 139.6917  # Tokyo
    print("City:", reverse_geocode(lat, lon))
