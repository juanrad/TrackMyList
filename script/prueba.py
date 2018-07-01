#!/usr/bin/env python3

import sys
import os
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth


def _cache_path(username):
    return os.path.join(os.curdir, '.cache-' + username)


def obtain_token(username):
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
        sp_oauth = SpotifyOAuth(client_id, client_secret, client_redirect_uri, cache_path=_cache_path(username),
                                scope=scope)
        info_token = sp_oauth.get_cached_token()
        if info_token:
            _token = info_token['access_token']

        # Prompt
        if not _token:
            _token = util.prompt_for_user_token(username, scope=scope, client_id=client_id, client_secret=client_secret,
                                                redirect_uri=client_redirect_uri)
    except Exception as e:
        cachepath = _cache_path(username)
        if os.path.exists(cachepath):
            os.remove(cachepath)
        print("something bad happened: " + str(e))
        sys.exit(2)

    if not _token:
        print("I can't read the auth token for username " + username)
        sys.exit(2)
    return _token


def create_playlist(sp_object, username, name, tracks):
    """
    Create a private playlist given a username, a name for the playlist and a list of track ids
    """
    try:
        playlist = sp_object.user_playlist_create(username, name, False)
        resp = sp_object.user_playlist_add_tracks(username, playlist['id'], tracks)
    except spotipy.client.SpotifyException as e:
        print("Something goes wrong while creating playlist: " + str(e))
    return resp


if __name__ == '__main__':
    if len(sys.argv) < 1:
        print("You need to specify your username")
        print("usage: script.py <username>")
        sys.exit()

    user_name = sys.argv[1]
    token = obtain_token(user_name)
    sp = spotipy.Spotify(auth=token)

    results = sp.search(q='artic monkeys', limit=3)
    track_ids = list(map(lambda x: x['id'], results['tracks']['items']))

#    new_playlist = sp.user_playlist_create(user_name, "DevList", False)
#    response = sp.user_playlist_add_tracks(user_name, new_playlist['id'], track_ids)

    for i, t in enumerate(results['tracks']['items']):
        print('Creating playlist ... ', i, t['name'])
        create_playlist(sp, user_name, t['name'], [t['id']])
