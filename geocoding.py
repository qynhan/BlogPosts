import requests
from urllib.parse import urlencode, urlparse, parse_qsl

GOOGLE_API_KEY = "AIzaSyCYmJr1lFmk6ntM1ojnFuME9teopMPVrSs"

class GoogleMapsClient(object):
    lat = None
    lng = None
    data_type = 'json'
    location_query = None
    api_key = None

    def __init__(self, api_key=None, address_or_postal_code=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if api_key == None:
            raise Exception("API key is required")
        self.api_key = api_key
        self.location_query = address_or_postal_code
        if self.location_query != None:
            self.extract_lat_lng()

    def extract_lat_lng(self, location=None):
        loc_query = self.location_query
        if location != None:
            loc_query = location
        endpoint = f"https://maps.googleapis.com/maps/api/geocode/{self.data_type}"
        params = {"address": loc_query, "key": self.api_key}
        url_params = urlencode(params)
        url = f"{endpoint}?{url_params}"
        r = requests.get(url)
        if r.status_code not in range(200, 299):
            return {}
        latlng = {}
        try:
            latlng = r.json()['results'][0]['geometry']['location']
        except:
            pass
        lat,lng = latlng.get("lat"), latlng.get("lng")
        self.lat = lat
        self.lng = lng
        return lat, lng

    def search(self, keyword="Mexican food", radius=5000, location=None):
        lat, lng = self.lat, self.lng
        if location != None:
            lat, lng = self.extract_lat_lng(location=location)
        endpoint = f"https://maps.googleapis.com/maps/api/place/nearbysearch/{self.data_type}"
        params = {
            "key": self.api_key,
            "location": f"{lat},{lng}",
            "radius": radius,
            "keyword": keyword
        }
        params_encoded = urlencode(params)
        places_url = f"{endpoint}?{params_encoded}"
        r = requests.get(places_url)
        # print(places_url, r.text)
        if r.status_code not in range(200, 299):
            return {}
        return r.json()

    def detail(self, place_id="ChIJlXOKcDC3j4ARzal-5j-p-FY", fields=["name", "formatted_phone_number", "formatted_address"]):
        detail_base_endpoint = f"https://maps.googleapis.com/maps/api/place/details/{self.data_type}"
        detail_params = {
            "place_id": f"{place_id}",
            "fields" : ",".join(fields),
            "key": self.api_key
        }
        detail_params_encoded = urlencode(detail_params)
        detail_url = f"{detail_base_endpoint}?{detail_params_encoded}"
        r = requests.get(detail_url)
        if r.status_code not in range(200, 299):
            return {}
        return r.json()

# format to use for the two methods
# client.search("Toys", radius=1500, location='15425 111 Ave Surrey')
# client.detail(place_id = 'ChIJVVVVyRLXhVQR_E3xjqhX_q4')
