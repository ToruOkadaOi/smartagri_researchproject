import requests

def geocode(address):
    url = f"https://nominatim.openstreetmap.org/search?format=json&limit=1&q={address}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data:
            latitude = data[0].get('lat')
            longitude = data[0].get('lon')
            return latitude, longitude
        else:
            return None, None
    else:
        return None, None

# Example usage:
address = "Alte Akademie 8 85354 Freising"

latitude, longitude = geocode(address)
if latitude is not None and longitude is not None:
    print("Latitude:", latitude)
    print("Longitude:", longitude)
else:
    print("Geocoding failed.")