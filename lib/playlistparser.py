import re
from codecs import open
from html.parser import HTMLParser
import requests


class ParseError(RuntimeError):
    def __init__(self, msg):
        self.msg = msg


class LaneHTMLParser(HTMLParser):

    def __init__(self, url=None, html_file=None):
        self.url = url
        self.html_file = html_file
        self.track_list = []
        self.cached_title = ''
        super().__init__()

    def parse(self):
        if self.url:
            self._parse_url()
        elif self.html_file:
            self._parse_file()
        else:
            raise ParseError("You must provide an url or an html file to the parser")

    def _parse_url(self):
        web = requests.get(self.url)
        self.feed(web.content.decode())

    def _parse_html_file(self):
        with open(self.html_file, 'r') as f:
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