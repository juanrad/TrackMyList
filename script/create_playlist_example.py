#!/usr/bin/env python3

import sys
from lib.spotipytools import SpotipyTools

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("You need to specify your username, a song and an artist")
        print("usage: script.py <username> <song> <artist>")
        sys.exit()

    username = sys.argv[1]
    song = sys.argv[2]
    artist = sys.argv[3]

    sptools = SpotipyTools(username)
    track = sptools.search(song, artist)
    sptools.create_playlist(username+'_creates_'+song, [track])


