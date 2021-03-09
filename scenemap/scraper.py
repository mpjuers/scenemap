#!/usr/bin/env python3

# Web scraper for music data.

# import asyncio as io
import base64
import itertools as it
import json
import os


import jsonmerge as jsm
import requests
from flask import request


class Scraper:

    # Authorization of application with spotify
    def __init__(self, username):
        # Client Keys
        self.CLIENT_ID = "e090b0487f5340d586563774981e37a7"
        self.CLIENT_SECRET = (
            "BQBb_D1gQ8f6e4iNQSbmvY_SiH_HJ3_xTa8MkOVVNnY2_KVKAlxFB7OcCNyr5e22SK_"
            "WZde1VooKubdujdHSNB_0tOzNMWEYthrgrdslQ35ipZ7gZ8udqoA-"
            "woK79elylygwNBewHeq04c5LajaJmopdvPhxmu_KLSrwO9OBgl7tmVXZZ0bufVDbIak"
        )
        message = f"{self.CLIENT_ID}: {self.CLIENT_SECRET}"
        messageBytes = message.encode("ascii")
        base64Bytes = base64.b64encode(messageBytes)
        self.message = base64Bytes.decode("ascii")

        # Spotify URLS
        self.SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
        self.SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
        self.SPOTIFY_API_BASE_URL = "https://api.spotify.com"
        self.API_VERSION = "v1"
        self.SPOTIFY_API_URL = "{}/{}".format(
            self.SPOTIFY_API_BASE_URL, self.API_VERSION
        )

        # Server-side Parameters
        self.CLIENT_SIDE_URL = "http://127.0.0.1"
        self.PORT = 8080
        self.REDIRECT_URI = "{}:{}/callback/q".format(
            self.CLIENT_SIDE_URL, self.PORT
        )
        self.SCOPE = "user-library-read"
        self.STATE = ""
        self.SHOW_DIALOG_bool = True
        self.SHOW_DIALOG_str = str(self.SHOW_DIALOG_bool).lower()
        self.path = os.path.expanduser("~")
# User info
        self.profile = username
        self.headers = {"Authorization": self.message}

    def app_Authorization(self):
        auth_query_parameters = {
            "response_type": "code",
            "redirect_uri": self.REDIRECT_URI,
            "scope": self.SCOPE,
            # "state": STATE,
            # "show_dialog": SHOW_DIALOG_str,
            "client_id": self.CLIENT_ID,
        }
        url_args = "&".join(
            [
                "{}={}".format(key, self.urllib.quote(val))
                for key, val in auth_query_parameters.iteritems()
            ]
        )
        auth_url = "{}/?{}".format(self.SPOTIFY_AUTH_URL, url_args)
        return auth_url

    # -----------------------------------------------------------------------------
    # The enclosed functions are from
    # https://github.com/bellerb/Spotify_Flask/blob/master/spotify.py
    # -----------------------------------------------------------------------------
    # User allows us to acces their spotify

    def user_authorization(self):
        auth_token = request.args["code"]
        code_payload = {
            "grant_type": "authorization_code",
            "code": str(auth_token),
            "redirect_uri": self.REDIRECT_URI,
        }

        # Tokens are Returned to Application
        # response_data = json.loads(post_request.text)
        # access_token = response_data["access_token"]
        # refresh_token = response_data["refresh_token"]
        # token_type = response_data["token_type"]
        # expires_in = response_data["expires_in"]
        post_request = requests.post(
            self.SPOTIFY_TOKEN_URL, data=code_payload, headers=self.headers
        )

        # Use the access token to access Spotify API
        authorization_header = self.message
        return authorization_header

    # Gathering of playlist information
    def playlist_data(self):
        # Get user playlist data
        playlist_api_endpoint = "{}/playlists".format(self.profile)
        playlists_response = requests.get(
            f"{self.SPOTIFY_API_BASE_URL}/{playlist_api_endpoint}",
            headers=self.headers
        )
        playlist_data = json.loads(playlists_response.text)
        return playlist_data

    # Gathering of album information
    def album_data(self, limit=1000):
        # Get user albums data
        artist_api_endpoint = (
            self.SPOTIFY_API_BASE_URL + "/{}/albums?limit=" + str(limit) + "&offset=0"
        ).format(self.profile)
        artist_response = requests.get(artist_api_endpoint, headers=self.headers)
        artist_data = json.loads(artist_response.text)
        return artist_data

    def get_tracks(self):

        tracks_albums = {}
        for album in self.album_data():
            print(album)
            # tracks_albums += json.loads(
            #     requests.get(
            #         (
            #             self.SPOTIFY_API_BASE_URL + "/"
            #             + album["artists"]["name"]
            #             + "/tracks"
            #         ),
            #         {"Authorization": self.CLIENT_SECRET},
            #     ).text
            # )
            # album_tracks_merged = jsm.merge(*tracks_albums).json

        tracks_playlists = {}
        for playlist in self.playlist_data():
            print(playlist)
            # tracks_playlists += json.loads(
            #     requests.get(
            #         "https://api.spotify.com/v1/playlists/"
            #         + playlist["items"]["artists"]["name"]
            #         + "/tracks",
            #         headers=self.header
            #     ).text
            # playlist_tracks_merged = jsm.merge(*tracks_albums).json
            # )

            # playlist_tracks_merged = jsm.merge(*tracks_playlists)

            # return jsm.merge(*album_tracks_merged, *playlist_tracks_merged)


def main():
    out = Scraper("mpjuers")
    out.get_tracks()


if __name__ == "__main__":
    main()
