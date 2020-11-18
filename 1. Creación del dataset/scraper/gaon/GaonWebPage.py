import urllib.parse

from gaon.GaonParser import GaonParser
from gaon.GaonStructuredData import GaonStructuredData


class GaonWebPage:

    def __init__(self, html=None, year_month=None):
        self.parser = GaonParser(html)
        self.year_month = year_month
        self.songs = GaonStructuredData()

    def get_all_monthly_links_text(self, until):
        texts = self.parser.get_monthly_links_text()
        texts = [t for t in texts if int(t[:4]) > int(until)]
        return texts

    def build_link_params(self):
        year = self.year_month[:4]
        month = self.year_month[4:]
        params = {"targetTime": month, "hitYear": year, "termGbn": "month"}
        params = urllib.parse.urlencode(params)
        return params

    def get_songs(self):
        songs, distributor = self.parser.get_songs()
        quantity = int(len(songs) * 0.25)  # popular is 25% of the top,
        # unpopular is 25% of the bottom
        songs = songs[:quantity] + songs[-quantity:]
        distributor = distributor[:quantity] + distributor[-quantity:]
        songs_info = {"title": [],
                      "singer": [],
                      "album": [],
                      "producer": [],
                      "distributor": [],
                      "external_factors": [0] * (len(songs))}

        for s, d in zip(songs, distributor):
            songs_info['title'].append(self.parser.get_song_title(s))
            songs_info['singer'].append(self.parser.get_song_singer(s))
            songs_info['album'].append(self.parser.get_song_album(s))
            songs_info['producer'].append(self.parser.get_song_producer(d))
            songs_info['distributor'].append(self.parser.get_song_distributor(d))
        songs_info['year_month'] = [self.year_month] * len(songs)
        songs_info['num_times_top_10'] = [1] * 10 + [0] * (len(songs) - 10)
        songs_info['num_times_top_5'] = [1] * 5 + [0] * (len(songs) - 5)
        songs_info['num_times_top_1'] = [1] + [0] * (len(songs) - 1)
        songs_info['is_popular'] = ['1'] * quantity + ['0'] * quantity
        self.songs.initialize(songs_info)
        return self.songs

    def set_html(self, html):
        self.parser.set_html(html)
