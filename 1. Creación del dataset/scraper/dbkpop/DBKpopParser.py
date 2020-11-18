class DBKpopParser():

    def __init__(self, html):
        self.html = html

    def get_table_header_strings(self):
        header_texts = self.html.find('table').find_all('th')
        seen = set()
        header_texts = [x.text for x in header_texts if not (x.text in seen or
                                                             seen.add(x.text))]
        header_texts = [x.strip().lower().replace(" ", "_") for x in
                        header_texts]
        return header_texts

    def get_table_rows(self):
        return self.html.find('tbody').find_all('tr')

    def get_data_from_row(self, row):
        tds = row.find_all('td')
        tds = [x.text.strip() for x in tds]
        return tds
