import multiprocessing as mp
import time

import nltk

from config import config
from util.logger import log


def clean_up_text(df, column_name):
    log.info('Starting Text Cleanup')
    TextCleaner().set_up_nltk()
    start_time = time.time()
    with mp.Pool() as pool:
        result = pool.map(TextCleaner().strip, df[column_name])
    log.info("Finished Text Clean up after %s seconds" % (time.time() - start_time))
    return result


class TextCleaner:
    __set_up = False

    # todo @pandermatt read https://www.machinelearningplus.com/nlp/lemmatization-examples-python/
    def strip(self, text):
        tokens = nltk.word_tokenize(text.lower())
        lemmatizer = nltk.WordNetLemmatizer()

        tokens = [t for t in tokens if
                  t not in nltk.corpus.stopwords.words(config.get_env('DATA_LANGUAGE')) and t.isalpha()]
        tokens = [lemmatizer.lemmatize(t, self.wordnet_pos(t)) for t in tokens]
        return ' '.join(tokens)

    def wordnet_pos(self, word):
        tag = nltk.pos_tag([word])[0][1][0].upper()
        tag_dict = {"J": nltk.corpus.wordnet.ADJ,
                    "N": nltk.corpus.wordnet.NOUN,
                    "V": nltk.corpus.wordnet.VERB,
                    "R": nltk.corpus.wordnet.ADV}

        return tag_dict.get(tag, nltk.wordnet.NOUN)

    def set_up_nltk(self):
        if not self.__set_up:
            return
        self.__set_up = True

        nltk.download('punkt')
        nltk.download('averaged_perceptron_tagger')
        nltk.download('maxent_ne_chunker')
        nltk.download('words')
        nltk.download('wordnet')
        nltk.download('stopwords')
