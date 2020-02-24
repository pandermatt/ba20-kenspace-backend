import nltk

from util.timed_cache import timed_cache


def extract_nouns(df, column_name):
    return df[column_name].apply(lambda x: NounExtraction().get_continuous_chunks(x)).tolist()


class NounExtraction:
    __set_up = False

    @timed_cache(minutes=10)
    def get_continuous_chunks(self, text, chunk_func=nltk.ne_chunk):
        """
        Source: https://stackoverflow.com/a/49584275
        """

        self.__set_up_nltk()

        try:
            chunked = chunk_func(nltk.pos_tag(nltk.word_tokenize(text)))
            continuous_chunk = []
            current_chunk = []
            for subtree in chunked:
                if type(subtree) == nltk.Tree:
                    current_chunk.append(" ".join([token for token, pos in subtree.leaves()]))
                elif current_chunk:
                    named_entity = " ".join(current_chunk)
                    if named_entity not in continuous_chunk:
                        continuous_chunk.append(named_entity)
                        current_chunk = []
                else:
                    continue

            continuous_chunk = " ".join(continuous_chunk)
            print(continuous_chunk)
        except TypeError:
            continuous_chunk = ''
        return continuous_chunk

    def __set_up_nltk(self):
        if not self.__set_up:
            return
        self.__set_up = True

        nltk.download('punkt')
        nltk.download('averaged_perceptron_tagger')
        nltk.download('maxent_ne_chunker')
        nltk.download('words')
