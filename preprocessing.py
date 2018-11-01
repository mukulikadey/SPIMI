import nltk
import string
from nltk.corpus import stopwords

def preprocess(documents):
    # Tokenize each word in documents
    for key in documents.keys():
        tokens = nltk.word_tokenize((documents[key]))
        processed_tokens = normalize(tokens)
        documents[key] = processed_tokens

    return documents


def normalize(tokens):
    # nltk.download('stopwords')
    stops = list(set(stopwords.words("english")))
    stops_30 = stops[:30]
    stops_150 = stops[:150]

    processed_tokens = tokens
    # -- 1. Discard Tokens with punctuation marks
    processed_tokens = [token for token in processed_tokens if not token in string.punctuation]
    # -- 2. Discard blank tokens
    processed_tokens = filter(None, processed_tokens)
    processed_tokens = [token for token in processed_tokens if not token == "''" and not token == '``']
    # -- 3. Discard tokens that are digits
    processed_tokens = [token for token in processed_tokens if not token.isdigit()]
    processed_tokens = [token for token in processed_tokens if token.isalpha()]
    # -- 4. Discard tokens which are stopwords
    processed_tokens = [token for token in processed_tokens if not token in stops]
    # processed_tokens = [token for token in processed_tokens if not token in stops_150]
    # processed_tokens = [token for token in processed_tokens if not token in stops_30]
    # -- 5. Apply lowercase to all tokens
    processed_tokens = [token.lower() for token in processed_tokens]

    return processed_tokens

