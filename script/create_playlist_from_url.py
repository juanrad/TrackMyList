import sys

import spotipytools
from playlistparser import LaneHTMLParser
from spotipytools import SpotipyTools

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("You need to specify a valid url and your username")
        print("usage: script.py <url.html> <username>")
        sys.exit()

    url = sys.argv[1]
    username = sys.argv[2]

    print("")
    print("Reading webpage...")
    parser = LaneHTMLParser(url=url)
    parser.parse()
    print("Done!")

    print("")
    print("I found "+str(len(parser.track_list))+" tracks, begining with...")
    num = 0
    for track in parser.track_list[0:10]:
        print("\t"+str(num)+": "+track['title']+" - "+track['artist'])
        num += 1
    print("")
    sptools = SpotipyTools(username)
    while True:
        user_input = input("Shall I create a playlist? (yes or no?): ")
        if user_input.lower()[0] in ['y', 'n']:
            name = input('Write the name of the playlist:')
            first_track = int(input('Show the above list. Which number is the first track?:'))
            parser.track_list = parser.track_list[first_track:-1]

            print("Finding tracks in spotify...")
            tracks_found = []
            for track in parser.track_list:
                try:
                    print("\t\t"+track['title']+" - "+track['artist']+" ... ", end='')
                    tracks_found.append(sptools.search(track['title'], track['artist']))
                    print("ok!")
                except spotipytools.TrackNotFound as e:
                    print("", flush=True)
                    print("\t\t\t", e.msg, file=sys.stderr, flush=True)
                    next

            sptools.create_playlist(name, tracks_found)
            break
        else:
            print('That is not a valid option!')
    print("")
    print("Done!")

