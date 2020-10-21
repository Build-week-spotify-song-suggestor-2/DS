import os
import base64
import datetime
import requests
from dotenv import load_dotenv
load_dotenv()

BASE_URL = "https://api.spotify.com/v1"
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")


class SpotifyClient:

  def get_client_credentials(self):
    """
    Returns base64 encoded string.
    """
    if SPOTIFY_CLIENT_ID is None or SPOTIFY_CLIENT_SECRET is None:
      raise Exception("SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET not found.")
    credentials = f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}"
    return base64.b64encode(credentials.encode()).decode()

  def authenticate(self):
    """
    Request client credentials.
    """
    res = requests.post(
      'https://accounts.spotify.com/api/token',
      data = {"grant_type": "client_credentials"},
      headers = {"Authorization": f"Basic {self.get_client_credentials()}"})

    if res.status_code not in range(200, 300):
      return False

    data = res.json()
    self.access_token_expires = datetime.datetime.now() + \
      datetime.timedelta(seconds=data["expires_in"])
    self.access_token = data["access_token"]
    return True

  def request_track_ids(self, title, artist):
    """
    Produces ids for all tracks found that have the specified title and artist.
    """
    res = requests.get(
      f"{BASE_URL}/search",
      params={"q": title, "type": "track"},
      headers={"Authorization": f"Bearer {self.access_token}"}
    )

    if res.status_code not in range(200, 300):
      if not self.authenticate():
        return False

    return [track["id"] for track in res.json()["tracks"]["items"]
      if artist.lower() in [artist["name"].lower() for artist in track["artists"]]]

  def request_track_info(self, track_id):
    """
    Produces the title and artist for the track with the specified id.
    """
    res = requests.get(
      f"{BASE_URL}/tracks/{track_id}",
      headers={"Authorization": f"Bearer {self.access_token}"}
    )

    if res.status_code not in range(200, 300):
      title = None
      artists = []
    else:
      track_info = res.json()
      title = track_info["name"]
      artists = [artist['name'] for artist in track_info['artists']]

    return {
      "title": title,
      "artists": artists
    }


client = SpotifyClient()
client.authenticate()
