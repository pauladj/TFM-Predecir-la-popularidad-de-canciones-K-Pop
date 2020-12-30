from dbkpop.DBKpopParser import DBKpopParser
from dbkpop.StructuredData import StructuredData


class DBKpopPage():
    def __init__(self, html):
        self.parser = DBKpopParser(html)

    def get_table_columns(self):
        """
        Get table header strings
        """
        return self.parser.get_table_header_strings()

    def get_table(self):
        # Get table data
        table_columns = self.get_table_columns()
        table_data = dict.fromkeys(table_columns, [])
        rows = self.parser.get_table_rows()
        for j, r in enumerate(rows):
            # For every row get the data as a list
            texts = self.parser.get_data_from_row(r)
            for i, t in enumerate(texts):
                # For every cell get the value and save it on a list. One
                # for each column.
                row_values = table_data[table_columns[i]]
                if j == 0:
                    row_values = []
                    table_data[table_columns[i]] = row_values
                row_values.append(t)

        # Initialize dataframe
        s = StructuredData()
        s.initialize(table_data)
        return s
