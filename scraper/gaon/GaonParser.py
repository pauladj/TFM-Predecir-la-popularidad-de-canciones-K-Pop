class GaonParser:

    def __init__(self, html=None):
        self.html = html

    def set_html(self, html):
        self.html = html

    def get_songs(self):
        songs_info = self.html.find_all('td', {"class": "subject"})
        production_info = self.html.find_all('td', {"class": "production"})
        return songs_info, production_info

    def get_productor(self):
        production = self.html.find_all('td', {"class": "production"})
        text = production.find('p', {'class': 'pro'}).text
        return text

    def get_monthly_links_text(self):
        options = []
        select_element = self.html.find('select', id="chart_month_select")
        if select_element:
            options = select_element.find_all('option')
        options = [x['value'] for x in options if x['value']]
        return options

    def get_song_title(self, html):
        return html.find('p').text

    def get_song_singer(self, html):
        text = html.find('p', {'class': 'singer'}).text
        if "|" in text:
            text = text.split("|")[0]
        return text

    def get_song_album(self, html):
        text = html.find('p', {'class': 'singer'}).text
        if "|" in text:
            text = text.split("|")
            if len(text) == 2:
                text = text[1]
            else:
                text = None
        return text

    def get_song_producer(self, html):
        text = html.find('p', {'class': 'pro'}).text
        return text

    def get_song_distributor(self, html):
        text = html.find('p', {'class': 'dist'}).text
        return text
