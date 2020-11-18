from dbkpop.DBKpopPage import DBKpopPage
from utils import PageRequester


class DBKpopManager:

    def __init__(self, data_folder):
        self.data_folder = data_folder

    def save_k_pop_table(self, url, file_name):
        """
        Extract and save one table as csv file
        :param url: The page url
        :param file_name: The output file
        """
        requester = PageRequester()
        html = requester.get(url) 
        p = DBKpopPage(html)
        data = p.get_table()
        data.save_as(f"{self.data_folder}/{file_name}")
