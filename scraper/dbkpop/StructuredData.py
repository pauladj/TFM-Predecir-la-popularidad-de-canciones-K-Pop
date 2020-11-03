import pandas as pd


class StructuredData:

    def __init__(self, data=None):
        self.data = data

    def initialize(self, value_dict):
        self.data = pd.DataFrame(value_dict, columns=value_dict.keys())

    def save_as(self, file):
        """

        :param file:
        :return:
        """
        if self.data is not None:
            self.data.to_csv(file, index=False)
