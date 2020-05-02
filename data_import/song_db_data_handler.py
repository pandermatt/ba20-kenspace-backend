import pandas as pd

from config import config
from data_import.data_handler import DataHandler


class SongDbDataHandler(DataHandler):
    """
    Dataset Source:
    https://www.kaggle.com/rakannimer/billboard-lyrics#billboard_lyrics_1964-2015.csv
    """

    def __init__(self):
        DataHandler.__init__(self, 'Song DB')
        path = config.input_data_file('billboard_lyrics_1964-2015.csv')
        self.df = pd.read_csv(path)
        self.df = self.df[self.df['Year'] >= 2000]
        self.df = self.df.fillna('')
        self.saved_item_to_cluster = [i + j for i, j in zip(self.clean_up_df_text('Song'),
                                                            self.clean_up_df_text('Lyrics'))]

    def display_labels(self):
        return ('"'
                + self.df['Song'].str.capitalize()
                + '" - '
                + self.df['Artist'].str.capitalize()
                ).tolist()

    def meta_info(self):
        contents = self.df['Lyrics'].tolist()
        release_dates = self.df['Year'].tolist()

        return [{
            "content": content,
            "release_date": release_date
        } for content, release_date in zip(contents, release_dates)]
