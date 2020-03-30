import random

import pandas as pd
from faker import Faker

from config import config
from data_import.data_handler import DataHandler


class WhatsAppDataHandler(DataHandler):
    __columns = ['From', 'Content']

    def __init__(self):
        DataHandler.__init__(self, 'WhatsApp')
        input_data = config.input_data_file('_chat.txt')

        fake = Faker(['de_DE', 'en_US'])

        rows = []
        # name_map = {}
        names = [fake.first_name() for _ in range(10)]
        with open(input_data) as fp:
            while True:
                row = [''] * 2

                line = fp.readline()
                if not line:
                    break
                line = ''.join(line.split("]")[1:]).strip()

                if len(line.split(":")) < 2:
                    continue

                # name = line.split(":")[0]
                # if name not in name_map:
                #     name_map[name] = fake.first_name()

                # row[0] = name_map[name]
                row[0] = random.choice(names)
                row[1] = ''.join(line.split(":")[1:]).strip()

                rows.append(row)

        df = pd.DataFrame(rows, columns=self.__columns)
        df['combined'] = df['From'].astype(str) + ': ' + df['Content']
        self.df = df.fillna('')
        self.saved_item_to_cluster = self.clean_up_df_text('combined', language="german")

    def display_labels(self):
        return self.df['Content'].tolist()

    def meta_info(self):
        return [{"content": f'from {content}'} for content in self.df['From'].tolist()]

    def calculate_n_clusters(self):
        return 1000


if __name__ == '__main__':
    WhatsAppDataHandler()
