import sys
import os
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth


class TrackNotFound(RuntimeError):
    def __init__(self, msg):
        self.msg = msg


class SpotipyTools:

    def __init__(self, username):
        self.username = username
        self.cache_path = os.path.join(os.curdir, '.cache-' + self.username)
        self.token = self.obtain_token()
        self.sp = spotipy.Spotify(auth=self.token)

    def obtain_token(self):
        """
        Obtain token from Oauth protocol: ask user to paste the redirect uri.
        Uses a cache for avoiding ask user too many times.
        :return: Str token or raise an exception
        """
        client_id = os.getenv('SPOTIPY_CLIENT_ID')
        client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
        client_redirect_uri = os.getenv('SPOTIPY_REDIRECT_URI')
        scope = 'playlist-modify-private'

        _token = ''
        try:
            # Cache
            sp_oauth = SpotifyOAuth(client_id, client_secret, client_redirect_uri,
                                    cache_path=self.cache_path, scope=scope)
            info_token = sp_oauth.get_cached_token()
            if info_token:
                _token = info_token['access_token']

            # Prompt
            if not _token:
                _token = util.prompt_for_user_token(self.username, scope=scope, client_id=client_id,
                                                    client_secret=client_secret, redirect_uri=client_redirect_uri)
        except Exception as e:
            if os.path.exists(self.cache_path):
                os.remove(self.cache_path)
            print("something bad happened: " + str(e))
            sys.exit(2)

        if not _token:
            print("I can't read the auth token for username " + self.username)
            sys.exit(2)
        return _token

    def create_playlist(self, name, tracks):
        """
        Create a private playlist given a username, a name for the playlist and a list of track ids.
        Due to Spotify API limitations, large playlist will be divided into ~100 tracks-list.
        - name: Str, name for the new playlist
        - tracks: list of tracks ids
        """
        nmax = 100;
        try:
            playlist = self.sp.user_playlist_create(self.username, name, False)
            n = 0
            while len(tracks[n:nmax]) > 0:
                subset = tracks[n:nmax]
                resp = self.sp.user_playlist_add_tracks(self.username, playlist['id'],
                                                        [track['id'] for track in subset])
                n += nmax
        except spotipy.client.SpotifyException as e:
            print("Something goes wrong while creating playlist: " + str(e))
        return resp

    def search(self, song, artist):
        """
        search a track given a song name and an artist
        :return: a track, duh
        """
        query = 'name:' + song + '&artist:' + artist
        response = self.sp.search(q=song + ' ' + artist, limit=1)
        results = response['tracks']['items']
        if len(results) == 0:
            error_message = "I can't find a track whith the name " + song + " for the artist " + artist
            raise TrackNotFound(error_message)
        return results[0]
