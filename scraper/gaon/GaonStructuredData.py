import pandas as pd

from scraper.dbkpop.StructuredData import StructuredData


class GaonStructuredData(StructuredData):

    def concatenate(self, data_aux):
        if self.data is not None:
            production_dictionary = pd.concat([self.data[['title', 'singer',
                                                          'producer',
                                                          'distributor']],
                                               data_aux.data[
                                                   ['title', 'singer',
                                                    'producer',
                                                    'distributor']]])
            self.data.drop(['producer', 'distributor'],
                           axis=1, inplace=True)
        else:
            production_dictionary = data_aux.data[['title', 'singer',
                                                   'producer', 'distributor']]

        production_dictionary = production_dictionary.drop_duplicates(subset=[
            'title', 'singer'], keep='first')
        data_aux.data.drop(['producer', 'distributor'],
                           axis=1, inplace=True)
        self.data = pd.concat([self.data, data_aux.data])
        self.data = pd.merge(self.data, production_dictionary, how='inner')

        self.data = self.data.groupby(['title', 'singer', 'album',
                                       'producer', 'distributor']).agg(
            {
                'year_month': '-'.join,
                'is_popular': '-'.join,
                'external_factors': 'sum',
                'num_times_top_10': 'sum',
                'num_times_top_5': 'sum',
                'num_times_top_1': 'sum'}).reset_index()

        popular_to_no_popular = self.data.query('is_popular == "1-0"')
        self.data.loc[popular_to_no_popular.index, 'is_popular'] = '1'
        self.data.loc[popular_to_no_popular.index, 'year_month'] = \
            self.data.loc[
                popular_to_no_popular.index, 'year_month'].str.replace(
                r'(-?\d+)$', '')

        remaining_rows_idx = self.data.index.difference(
            popular_to_no_popular.index)
        no_popular_to_popular = self.data.iloc[remaining_rows_idx].query(
            'is_popular == "0-1"')
        self.data.loc[no_popular_to_popular.index, 'is_popular'] = '1'
        self.data.loc[no_popular_to_popular.index, 'external_factors'] = 1
        self.data.loc[no_popular_to_popular.index, 'year_month'] = \
            self.data.loc[
                no_popular_to_popular.index, 'year_month'].str.replace(
                r'(\d+-)', '')

        remaining_rows_idx = remaining_rows_idx.difference(
            no_popular_to_popular.index)
        popular_to_popular = self.data.iloc[remaining_rows_idx].query(
            'is_popular == "1-1"')
        self.data.loc[popular_to_popular.index, 'is_popular'] = '1'

        remaining_rows_idx = remaining_rows_idx.difference(
            popular_to_popular.index)
        no_popular_to_no_popular = self.data.iloc[remaining_rows_idx].query(
            'is_popular == "0-0"')
        self.data.loc[no_popular_to_no_popular.index, 'is_popular'] = '0'
