import spimi
import reuters
import preprocessing
from glob import iglob
import json
from spimi import SPIMI

def ranking(documents):

    num_documents = len(documents.keys())

    doc_len = {}
    sum_len = 0

    for docId, token_list in documents.items():
        length = len(token_list)
        doc_len[docId] = length
        sum_len += length

    avg_len = sum_len / num_documents

    bm25_param = {
        'N': num_documents,
        'Ld': doc_len,
        'Lave': avg_len
    }

    with open('bm25_param.txt', 'w') as f:
        json.dump(bm25_param, f)


if __name__ == '__main__':

    block_size_limit = 500
    print("Current block size limit: ", block_size_limit)
    print("=============== Retriving documents =============== ")
    documents = reuters.getDocuments()
    print("=============== Preprocessing documents ===========")
    documents = preprocessing.preprocess(documents)
    ranking(documents)
    print("=============== Applying SPIMI Algorithm ==========")
    spimi = SPIMI(block_size_limit, documents)
    spimi.invert()









