import sys

import spotipytools
from playlistparser import LaneHTMLParser
from spotipytools import SpotipyTools

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("You need to specify a file, your username, a song and an artist")
        print("usage: script.py <file.html> <username> <song> <artist>")
        sys.exit()

    html_file = sys.argv[1]
    username = sys.argv[2]
    song = sys.argv[3]
    artist = sys.argv[4]

    print("")
    print("Reading file...")
    parser = LaneHTMLParser(html_file)
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
        print("Shall I create a playlist?")
        user_input = input('Yes or No?: ')
        if user_input.lower()[0] in ['y', 'n']:
            name = input('Write the name of the playlist:')
            first_track = int(input('Show the above list. Which number is the first track?:'))
            parser.track_list = parser.track_list[first_track:-1]

            print("Finding tracks in spotify...")
            tracks_found = []
            for track in parser.track_list:
                try:
                    sp_track = sptools.search(track['title'], track['artist'])
                    tracks_found.append(sp_track['id'])
                except spotipytools.TrackNotFound as e:
                    print(e)
                    next

            sptools.create_playlist(name, tracks_found)
            break
        else:
            print('That is not a valid option!')
    print("")
    print("Done!")
