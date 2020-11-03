from scraper.dbkpop.DBKpopParser import DBKpopParser
from scraper.dbkpop.StructuredData import StructuredData


class DBKpopPage():
    def __init__(self, html):
        self.parser = DBKpopParser(html)

    def get_table_columns(self):
        return self.parser.get_table_header_strings()

    def get_table(self):
        # Get table data
        table_columns = self.get_table_columns()
        table_data = dict.fromkeys(table_columns, [])
        rows = self.parser.get_table_rows()
        for j, r in enumerate(rows):
            texts = self.parser.get_data_from_row(r)
            for i, t in enumerate(texts):
                row_values = table_data[table_columns[i]]
                if j == 0:
                    row_values = []
                    table_data[table_columns[i]] = row_values
                row_values.append(t)

        s = StructuredData()
        s.initialize(table_data)
        return s
