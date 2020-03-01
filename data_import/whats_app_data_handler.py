import pandas as pd

from config import config
from data_import.data_handler import DataHandler
from util.text_clean_up import clean_up_text
from util.timed_cache import timed_cache


class WhatsAppDataHandler(DataHandler):
    __columns = ['From', 'Content']

    def __init__(self):
        DataHandler.__init__(self, 'WhatsApp')
        input_data = config.input_data_file('_chat.txt')

        rows = []
        with open(input_data) as fp:
            while True:
                row = [''] * 2

                line = fp.readline()
                if not line:
                    break
                line = ''.join(line.split("]")[1:]).strip()
                row[0] = line.split(":")[0]
                row[1] = ''.join(line.split(":")[1:]).strip()

                rows.append(row)

        df = pd.DataFrame(rows, columns=self.__columns)
        df['combined'] = df['From'].astype(str) + ': ' + df['Content']
        self.df = df.fillna('')

    def display_labels(self):
        return self.df['combined'].tolist()

    @timed_cache(minutes=30)
    def __cached_cleanup(self, col):
        return clean_up_text(self.df, col)

    def content_labels(self):
        return self.__cached_cleanup('Content')

    def item_to_cluster(self):
        return self.__cached_cleanup('combined')


if __name__ == '__main__':
    WhatsAppDataHandler()
