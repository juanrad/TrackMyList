from codecs import open
from html.parser import HTMLParser
import re


class LaneHTMLParser(HTMLParser):

    def __init__(self, file):
        self.file = file
        self.track_list = []
        self.cached_title = ''
        super().__init__()

    def parse(self):
        with open(self.file, 'r') as f:
            read_data = f.read()
            self.feed(read_data)

    def handle_data(self, data):
        if not re.match(r'^\s+$', data) and not re.match(r'\d+\:\d', data) and data[0] != "\n":
            data = data.strip()
            if self.cached_title == '':
                # print('track: '+data)
                self.cached_title = data
            else:
                # print('artist: '+data)
                track = {'title': self.cached_title, 'artist': data}
                self.track_list.append(track)
                self.cached_title = ''