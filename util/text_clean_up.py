import multiprocessing as mp
import time

import nltk
import spacy

from config import config
from util.logger import log


def clean_up_text(df, column_name):
    log.info('Starting Text Cleanup')
    if config.get_env("PROCESSES_NUMBER") < 2:
        # for non multiprocessing OS
        return df[column_name].apply(lambda x: NltkTextCleaner().tokenizer(x)).tolist()
    start_time = time.time()
    with mp.Pool() as pool:
        result = pool.map(SpacyTextCleaner().tokenizer, df[column_name])
    log.info("Finished Text Clean up after %s seconds" % (time.time() - start_time))
    return result


class NltkTextCleaner:
    def __init__(self):
        nltk.download('punkt', quiet=True)
        nltk.download('averaged_perceptron_tagger', quiet=True)
        nltk.download('maxent_ne_chunker', quiet=True)
        nltk.download('words', quiet=True)
        nltk.download('wordnet', quiet=True)
        nltk.download('stopwords', quiet=True)

    # todo @pandermatt read https://www.machinelearningplus.com/nlp/lemmatization-examples-python/
    def tokenizer(self, text):
        tokens = nltk.word_tokenize(text.lower())
        lemmatizer = nltk.WordNetLemmatizer()

        tokens = [t for t in tokens if
                  t not in nltk.corpus.stopwords.words(config.get_env('DATA_LANGUAGE')) and t.isalpha()]
        tokens = [lemmatizer.lemmatize(t, self.wordnet_pos(t)) for t in tokens]
        return tokens

    def wordnet_pos(self, word):
        tag = nltk.pos_tag([word])[0][1][0].upper()
        tag_dict = {"J": nltk.corpus.wordnet.ADJ,
                    "N": nltk.corpus.wordnet.NOUN,
                    "V": nltk.corpus.wordnet.VERB,
                    "R": nltk.corpus.wordnet.ADV}

        return tag_dict.get(tag, nltk.wordnet.NOUN)


class SpacyTextCleaner:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def tokenizer(self, text):
        doc = self.nlp(text)
        # return [e.lemma_ for e in doc if e.is_alpha and not e.is_stop] + [e.text for e in doc.ents]
        return [e.text for e in doc.ents]

# def update_progress_bar():
#     global i, total
#     i += 1
#     progress_bar(i, total)
#
#
# def progress_bar(value, endvalue, bar_length=50):
#     percent = float(value) / endvalue
#     arrow = '-' * int(round(percent * bar_length) - 1) + '>'
#     spaces = ' ' * (bar_length - len(arrow))
#
#     sys.stdout.write("\rPercent: [{0}] {1}%".format(arrow + spaces, int(round(percent * 100))))
#     sys.stdout.flush()
