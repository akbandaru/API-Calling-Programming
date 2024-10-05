import requests
from bs4 import BeautifulSoup
import spotipy
import Env_var
from spotipy.oauth2 import SpotifyOAuth


date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

URL = "https://www.billboard.com/charts/hot-100/" + date
year = date.split("-")[0]

response = requests.get(URL)
soup = BeautifulSoup(response.text, "html.parser")
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="playlist-modify-private",
                                               redirect_uri="http://example.com",
                                               client_id=Env_var.CLIENT_ID,
                                               client_secret=Env_var.CLIENT_SECRET,
                                               show_dialog=True,
                                               cache_path="token.txt"))

song_list = [song.getText().strip() for song in soup.select("li ul li h3")]
print(song_list)
song_uris = []

user_id = sp.current_user()["id"]
print(user_id)

for song in song_list:
    result = sp.search(f"track: {song} year:{year}")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)








