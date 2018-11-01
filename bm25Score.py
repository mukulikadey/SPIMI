import json
import math

with open('bm25_param.txt', 'r') as f:
    bm25_param = json.load(f)

def get_score(query_params, k1, b):
    N = bm25_param['N']
    Ld = bm25_param['Ld']
    Lave = bm25_param['Lave']

    score = 0

    for query_param in query_params.values():
        dft = query_param['dft']
        tftd = query_param['tftd']
        docid = query_param['docid']

        idf = math.log(N / dft)
        other_weight = ((k1 + 1) * tftd) / (k1 * ((1-b) + b * (Ld[docid] / Lave)) + tftd)

        score += idf * other_weight

    return score