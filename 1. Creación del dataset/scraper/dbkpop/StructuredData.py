import pandas as pd


class StructuredData:

    def __init__(self, data=None):
        self.data = data

    def initialize(self, value_dict):
        """
        Initialize the dataset from a dictionary
        :param value_dict: dictionary with the data
        """
        self.data = pd.DataFrame(value_dict, columns=value_dict.keys())

    def save_as(self, file):
        """
        Save dataframe to csv
        :param file:
        """
        if self.data is not None:
            self.data.to_csv(file, index=False)
