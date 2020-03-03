import glob
import os

import pandas as pd

from config import config
from data_import.data_handler import DataHandler
from util.logger import log
from util.text_clean_up import clean_up_text
from util.timed_cache import timed_cache


class EmailDataHandler(DataHandler):
    __columns = ['From', 'To', 'Cc', 'Subject']
    __last_line = "X-FileName"

    def __init__(self):
        DataHandler.__init__(self, 'Email')
        mail_data_dir = config.input_data_file('mail-data')
        mail_to_analyze = 'inbox'
        mail_to_analyze_path = os.path.join(mail_data_dir, mail_to_analyze)

        rows = []
        for mail_file in glob.glob(os.path.join(mail_to_analyze_path, '*.')):
            with open(mail_file) as fp:
                row = [''] * len(self.__columns)
                content_line = False
                content = ""
                while True:
                    try:
                        line = fp.readline()

                        if content_line:
                            content += line.strip()
                        else:
                            for col in self.__columns:
                                if line.startswith(col):
                                    row[self.__columns.index(col)] = line.strip().replace(':', '').replace(col, '')
                                    continue

                            if line.startswith(self.__last_line):
                                content_line = True

                        if not line:
                            break
                    except Exception:
                        log.warn("Error in File Reader, skipping line")
                rows.append(row + [content])

        df = pd.DataFrame(rows, columns=self.__columns + ['Content'])
        df['combined'] = df['From'].astype(str) + ' ' + df['To'] + ' ' + \
                         df['Cc'] + ' ' + df['Subject'] + ' ' + df['Content']
        self.df = df.fillna('')

    def display_labels(self):
        return [[subject, content] for subject, content in
                zip(self.df['Subject'].tolist(), self.df['Content'].tolist())]

    @timed_cache(minutes=30)
    def __cached_cleanup(self, col):
        return clean_up_text(self.df, col)

    def item_to_cluster(self):
        return self.__cached_cleanup('combined')


if __name__ == '__main__':
    EmailDataHandler()
