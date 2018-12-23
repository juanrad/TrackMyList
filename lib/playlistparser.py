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

        self._set_playlist_name_pattern()

        self.author = None
        self.track_list = []
        self.found_song = False
        self.found_artist = False
        self.cached_title = None
        super().__init__()

    def parse(self):
        if self.url:
            self._parse_url()
        elif self.html_file:
            self._parse_file()
        else:
            raise ParseError("You must provide an url or an html file to the parser")

    def _set_playlist_name_pattern(self):
        iname = re.findall('playlist\/([^\/]+)\/', self.url)[0]
        iname_no_bars = re.sub('-', ' ', iname)
        self._playlist_name_pattern = re.compile(iname_no_bars, re.IGNORECASE)

    def _author_and_name(self, attr):
        try:
            list_info = next(attr[i] for i in range(0, len(attr)) if self._playlist_name_pattern.search(attr[i]))
        except Exception:
            return
        self.playlist_name = re.findall("listen,([\w\s]+),", list_info)[0]
        self.author = re.findall("listen,[\w\s]+,([\w\s]+)", list_info)[0]
        self.playlist_name.strip();
        self.author.strip();

    def _parse_url(self):
        web = requests.get(self.url)
        self.feed(web.text)

    def _parse_html_file(self):
        with open(self.html_file, 'r') as f:
            read_data = f.read()
            self.feed(read_data)

    def handle_starttag(self, tag, attributes):
        for attr in attributes:
            try:
                if any(re.search('album', attr[i]) for i in range(0, len(attr))):
                    self.found_song = True
                    self.found_artist = False
                    return
                elif any(re.search('artist', attr[i]) for i in range(0, len(attr))):
                    # TODO: here appears some interesnting json to parse in the future
                    self.found_song = False
                    self.found_artist = True
                    return
                if not self.author:
                    self._author_and_name(attr)
            except Exception:
                pass

    def handle_data(self, data):
        if not self.found_song and not self.found_artist:
            return
        try:
            if not re.match(r'^\s+$', data) and not re.match(r'\d+\:\d', data) and data[0] != "\n":
                data = data.strip()
                if self.found_song:
                    # print('track: '+data)
                    self.cached_title = data
                elif self.found_artist:
                    # print('artist: '+data)
                    if not self.cached_title:
                        return
                    track = {'title': self.cached_title, 'artist': data}
                    self.track_list.append(track)
                    self.cached_title = None
                # else:
                #     print("i dont know what is " + data)
        except Exception:
            pass