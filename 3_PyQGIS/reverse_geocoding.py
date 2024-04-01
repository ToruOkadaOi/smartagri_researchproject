import requests

def reverse_geocode(latitude, longitude, api_key=None):
    base_url = "https://nominatim.openstreetmap.org/reverse"
    params = {
        "format": "json",
        "lat": latitude,
        "lon": longitude,
        "zoom": 18,
        "addressdetails": 1
    }
    if api_key:
        params['key'] = api_key
    
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        address = data.get('display_name', 'Address not found')
        return address
    else:
        return f"Reverse geocoding failed. Status code: {response.status_code}"

# Example usage:
latitude = 49.05587
longitude = 12.062988
api_key = "YOUR_API_KEY"  # Replace with your actual API key if required

address = reverse_geocode(latitude, longitude, api_key)
print("Address:", address)
