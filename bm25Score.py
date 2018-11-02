import json
import math

with open('bm25_param.txt', 'r') as f:
    bm25_param = json.load(f)

def calculate_score(query_params, k1, b):
    # get number of docs, document length, and average length of documents
    num_documents = bm25_param['num_documents']
    doc_len = bm25_param['doc_len']
    avg_len = bm25_param['avg_len']
    bm25_score = 0

    for query_param in query_params.values():
        # for each query term and its doc_ids, get doc freq, term freq, and doc_id
        doc_freq = query_param['doc_freq']
        term_freq = query_param['term_freq']
        doc_id = query_param['doc_id']

        bm25_score += (math.log(num_documents / doc_freq))*(((k1 + 1) * term_freq) / (k1 * ((1-b) + b * (doc_len[doc_id] / avg_len)) + term_freq))

    return bm25_score