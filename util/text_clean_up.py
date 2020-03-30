import multiprocessing as mp
import time

import nltk
import spacy
from spacy.symbols import PERSON

from config import config
from util.logger import log


def clean_up_text(df, column_name, language, clean_up_method):
    log.info('Starting Text Cleanup')
    should_use_multiprocessing = config.get_env("PROCESSES_NUMBER") < 2
    log.info(f'Using {clean_up_method}. Language={language}')

    if clean_up_method == "nltk":
        class_to_use = NltkTextCleaner(language)
    elif clean_up_method == "spacy":
        if language not in ['english', 'german']:
            log.warn(f'SpaCy does not support {language}')
            return
        class_to_use = SpacyTextCleaner(language)
    else:
        log.warn(f'{clean_up_method} not found')
        return

    if should_use_multiprocessing:
        return df[column_name].apply(lambda x: class_to_use.tokenizer(x)).tolist()
    start_time = time.time()
    with mp.Pool() as pool:
        result = pool.map(class_to_use.tokenizer, df[column_name])
    log.info("Finished Text Clean up after %s seconds" % (time.time() - start_time))
    return result


class NltkTextCleaner:
    def __init__(self, language):
        log.info('Setup NLTK')
        nltk.download('punkt', quiet=True)
        nltk.download('averaged_perceptron_tagger', quiet=True)
        nltk.download('maxent_ne_chunker', quiet=True)
        nltk.download('words', quiet=True)
        nltk.download('wordnet', quiet=True)
        nltk.download('stopwords', quiet=True)
        self.language = language

    def tokenizer(self, text):
        tokens = nltk.word_tokenize(text.lower())
        lemmatizer = nltk.WordNetLemmatizer()

        tokens = [t for t in tokens if
                  t not in nltk.corpus.stopwords.words(self.language) and t.isalpha()]
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
    def __init__(self, language):
        log.info('Setup SpaCy')
        if language == "english":
            self.nlp = spacy.load("en_core_web_sm")
        elif language == "german":
            self.nlp = spacy.load("de_core_news_sm")

    def tokenizer(self, text):
        doc = self.nlp(text)

        keyword = PERSON
        return self.__tokenize_keyword(doc, keyword)

    def __tokenize_keyword(self, doc, keyword):
        tokens = []
        temp_arr = []
        for token in doc:
            if token.ent_type == keyword:
                temp_arr.append(str(token))
            elif str(token) == '-':
                tokens.append(str(token))
            elif len(temp_arr) > 0:
                tokens.append(" ".join(temp_arr).lower())
                temp_arr = []
            else:
                if not token.is_stop and token.is_alpha:
                    tokens.append(str(token).lower())
        return self.__merge_tokens(tokens)

    def __merge_tokens(self, tokens):
        for i in range(len(tokens)):
            for j in range(len(tokens)):
                if tokens[j] in tokens[i]:
                    tokens[j] = tokens[i]
                elif tokens[i] in tokens[j]:
                    tokens[i] = tokens[j]
        return self.__merge_prefix_name(tokens)

    @staticmethod
    def __merge_prefix_name(tokens):
        spacing = '-'
        result = []
        for i in range(len(tokens)):
            t = str(tokens[i])
            if t == spacing and 0 < i < len(tokens) - 1:
                element = str(tokens[i - 1]) + t + str(tokens[i + 1])
                result.append(element)
            elif t != spacing and i < len(tokens) - 1 and str(tokens[i + 1]) == spacing:
                continue
            elif t != spacing and i > 0 and str(tokens[i - 1]) == spacing:
                continue
            else:
                result.append(str(tokens[i]))
        return result
