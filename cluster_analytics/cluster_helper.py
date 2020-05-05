def identity_func(stopwords):
    def func(token):
        if stopwords and token in stopwords:
            return [token]
        return token

    return func
