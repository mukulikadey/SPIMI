from nltk.corpus import stopwords


def discard_non_alpha(tokens):
    return [token for token in tokens if token.isalpha()]


def discard_non_alphanum(tokens):
    return [token for token in tokens if token.isalnum()]


def lowercase_words(tokens):
    return [token.lower() for token in tokens]


def discard_30_stop_words(tokens):
    stops = list(set(stopwords.words('english')))
    stops = stops[:30]
    return [token for token in tokens if not token in stops]


def discard_150_stop_words(tokens):
    stops = list(set(stopwords.words('english')))
    stops = stops[:150]
    return [token for token in tokens if not token in stops]


def discard_stop_words(tokens):
    stops = list(set(stopwords.words('english')))
    return [token for token in tokens if not token in stops]


def all(tokens):
    tokens = discard_non_alpha(tokens)
    tokens = lowercase_words(tokens)
    tokens = discard_stop_words(tokens)
    return tokens