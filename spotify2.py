from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def write_to_file(data, file_name):
    """
    To write file, for me.
    """
    with open(file_name, "w", encoding = "utf-8") as file:
        json.dump(data, file, indent = 4, ensure_ascii = False)

#отримую токен
def get_token():
    """
    Get token.
    """
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers = headers, data = data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

#header
def get_auth_header(token):
    """
    Get header
    """
    return {"Authorization": "Bearer " + token}

#знаходжу інфу про артиста за назвою
def search_for_artist(token, artist_name):
    """
    Search artist
    """
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"

    query_url = url + query
    result = get(query_url, headers = headers)
    json_temp = json.loads(result.content)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        print("No artists with this name exists..")
        return None
    return json_result[0]

#шукаю топ 10 пісень артиста
def get_songs_by_artist(token, artist_id):
    """
    Serach songs.
    """
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = get(url, headers = headers)
    json_result = json.loads(result.content)["tracks"]
    name_s = [f"{idx + 1}. {song['name']}" for idx, song in enumerate(json_result)]
    return name_s

#топ 1 пісня
def get_top_one_song(name_s):
    """
    Search top one.
    """
    first = name_s[0]
    return first

#шукаю available markets
def search_for_markets(token, first):
    """
    Search markets
    """
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={first}&type=track"

    query_url = url + query
    result = get(query_url, headers = headers)
    json_result = json.loads(result.content)
    if len(json_result) == 0:
        print("No artists with this name exists, so no markets...")
        return None
    available_markets = json_result['tracks']['items'][0]['album']['available_markets']
    return available_markets

#зліплюю все до купи
def main():
    """
    Main function
    """
    print("Hello! Please write name of artist:")
    name = str(input())
    print("""Here are information about artist, which you can find:
    1. Name
    2. Type
    3. Artist ID
    4. Amount of followers
    5. Genres of music
    6. Popularity
    7. Top one song
    8. Top 10 songs
    9. Markets""")
    token = get_token()
    result = search_for_artist(token, name)
    artist_id = result["id"]
    songs = get_songs_by_artist(token, artist_id)
    top_one = get_top_one_song(songs)
    markets = search_for_markets(token, top_one)
    while True:
        answer = str(input("Enter the number of the information you want to display (or 'exit' to quit): "))
        if answer == "1":
            print(result["name"])
        elif answer == "2":
            print(result["type"])
        elif answer == "3":
            print(artist_id)
        elif answer == "4":
            print(result["followers"]["total"])
        elif answer == "5":
            print(result["genres"])
        elif answer == "6":
            print(result["popularity"])
        elif answer == "7":
            print(top_one)
        elif answer == "8":
            print(songs)
        elif answer == "9":
            print(markets)
        elif answer == "exit":
            break
        else:
            print("Invalid input. Please enter a number from 1 to 8, or 'exit' to quit.")
# token = get_token()
# result = search_for_artist(token, "ACDC")
# artist_id = result["id"]
# songs = get_songs_by_artist(token, artist_id)
# top_one = get_top_one_song(songs)
# # print(top_one)

# markets = search_for_markets(token, artist_id, top_one)
# write_to_file(markets, "artist.json")
# print(markets)
if __name__ == "__main__":
    main()
