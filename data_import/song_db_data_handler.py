import pandas as pd

from config import config
from data_import.data_handler import DataHandler


class SongDbDataHandler(DataHandler):
    def __init__(self):
        DataHandler.__init__(self, 'Song DB')
        path = config.input_data_file('billboard_lyrics_1964-2015.csv')
        self.df = pd.read_csv(path)
        # self.df = self.df[df['Rank'] <= 1]
        self.df = self.df[self.df['Year'] >= 2000]
        self.df = self.df.fillna('')
        self.saved_item_to_cluster = [i + j for i, j in zip(self.clean_up_df_text('Song'),
                                                            self.clean_up_df_text('Lyrics'))]

    def display_labels(self):
        return ('Rank '
                + self.df['Rank'].astype(str)
                + '. (Year ' + self.df['Year'].astype(str)
                + '): "'
                + self.df['Song'].str.capitalize()
                + '" - '
                + self.df['Artist'].str.capitalize()).tolist()

    def meta_info(self):
        return [{"content": content} for content in self.df['Lyrics'].tolist()]
