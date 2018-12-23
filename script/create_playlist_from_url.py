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
        if len(user_input) == 0 or user_input.lower()[0] not in ['y', 'n']:
            print("That is not a valid option!\n", flush=True)
            continue
        if user_input.lower()[0] == 'n':
            break
        if user_input.lower()[0] == 'y':
            default_name = parser.author + "'s " + parser.playlist_name
            name = input(
                "Write the name of the playlist: \n\t (Leave blank to use default: " + default_name + ")\n")
            if name == '':
                name = default_name
            first_track = input('Show the above list. Which number is the first track?: '
                                '\n\t(Leave blank for default: 0)\n')
            if first_track == '':
                first_track = 0
            first_track = int(first_track)
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
                except Exception as e:
                    print("", flush=True)
                    print("\t\t\t", "Unespected error: "+str(e), file=sys.stderr, flush=True)
                    next
            sptools.create_playlist(name, tracks_found)
            break
    print("")
    print("Done!")

