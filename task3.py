from spotify2 import get_token
from spotify2 import search_for_artist
from spotify2 import get_songs_by_artist
from spotify2 import get_top_one_song
from spotify2 import search_for_markets
from functools import lru_cache
from folium import plugins
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import pycountry
import folium

geolocator = Nominatim(user_agent="my_html")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds= 5)

@lru_cache(maxsize=None)
def get_location(name: str):
    """
    Get coordinates from location of city.
    """
    return geolocator.geocode(name)

def search_coord(available_markets):
    """
    Search name of countries.
    """
    # шукаю з маркетів назви країн
    countries = []
    for elem in available_markets:
        de_st = pycountry.countries.get(alpha_2=elem)
        if de_st is None:
            countries.append(None)
        else:
            countries.append(de_st.name)
    res = []
    for elem in countries:
        if elem is None:
            continue
        new_e = elem.split(",")
        res.append(new_e[0])
    return res

def create_map(res):
    """
    Function to create map.
    """
    all_count = res
    latitude = []
    longitude = []
    for point in res:
        try:
            location = get_location(point)
            if location is None:
                latitude.append(None)
                longitude.append(None)
            else:
                latitude.append(location.latitude)
                longitude.append(location.longitude)
        except AttributeError:
            latitude.append(None)
            longitude.append(None)

    if None in latitude or None in longitude:
        print("Warning: Some country locations could not be retrieved.")
        return
    Map = folium.Map(tiles="Stamen Terrain", location=[0, 0], zoom_start = 5)
    for lt, ln, ac in zip(latitude, longitude, all_count):
        Map.add_child(folium.Marker(location=[lt,ln],
                            popup=ac,
                            icon=folium.Icon(color = "pink")))
    Map.add_child(plugins.MiniMap())
    Map.add_child(plugins.Terminator())
    Map.save('templates/Spotify.html')
    return "DONE"

def allss(artist_name):
    """
    Main function
    """
    token = get_token()
    result = search_for_artist(token, artist_name)
    artist_id = result["id"]
    songs = get_songs_by_artist(token, artist_id)
    top_one = get_top_one_song(songs)
    available_markets = search_for_markets(token, top_one)
    countries = search_coord(available_markets)
    create_map(countries)
    print("DONE")

if __name__ == "__main__":
    allss(str(input("Enter name of artist: ")))
