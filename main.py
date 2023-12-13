import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pprint
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri="http://example.com",
                                               show_dialog=True,
                                               cache_path=".cache",
                                               scope="playlist-modify-private"))
user_id = sp.current_user()['id']

users_date = input("What year would you like to travel to? Type the date in this format YYYY-MM-DD")
response = requests.get(f"https://www.billboard.com/charts/hot-100/{users_date}")
data = response.text
soup = BeautifulSoup(data, "html.parser")

songs = soup.find_all(name='h3', id='title-of-a-story', class_='c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only')
artists = soup.find_all(class_='c-label a-no-trucate a-font-primary-s lrv-u-font-size-14@mobile-max u-line-height-normal@mobile-max u-letter-spacing-0021 lrv-u-display-block a-truncate-ellipsis-2line u-max-width-330 u-max-width-230@tablet-only')
song_list = []
for movie in songs:
    m = movie.getText().strip()
    song_list.append(m)

print(song_list)

artist_list = [artist.getText().strip() for artist in artists]

print(artist_list)


song_uri_list = []
year = users_date.split("-")[0]
for song in song_list:
    result = sp.search(q=song)
    try:
        uri = result['tracks']['items'][0]['uri']
        song_uri_list.append(uri)
    except IndexError:
        print(f"{song} was not found. Skipped")
        pass
print(song_uri_list)

playlist = sp.user_playlist_create(user=user_id, name=f"{year}Top 100 - Billboard", public=False)
sp.playlist_add_items(playlist_id=playlist['id'], items=song_uri_list)

