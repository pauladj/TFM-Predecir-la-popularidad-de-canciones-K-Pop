import requests
from bs4 import BeautifulSoup


class PageRequester:

    def get(self, url):
        """
        Get the html of a website
        :param url: The website url
        :return: The html
        """
        connect_timeout = 30.0
        read_timeout = 100.0
        cookies = None
        try:
            page = requests.get(url, cookies=cookies,
                                timeout=(connect_timeout, read_timeout))
            page.encoding = page.apparent_encoding
            page = page.text
            page_html = BeautifulSoup(page, 'html.parser')
        except requests.exceptions.RequestException as e:
            print("Error fetching the page {}: {}".format(url, e))
            page_html = None
        return page_html
