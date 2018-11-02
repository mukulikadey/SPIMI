import preprocessing
from glob import iglob
from collections import OrderedDict
import collections
import json
import bm25Score
import operator

# constants for calculating the BM25 score
k1 = 1.5
b = 0.8

# ===============READ SPIMI INDEX==================

def read_spimi_index():
    spimi_index = OrderedDict()
    files = []

    for file in iglob('DISK/BLOCK*.txt'):
        files.append(file)

    for file in files:
        with open(file, 'r') as f:
            block = json.load(f)

            # Check if any of these items were already added to the spimi_index
            # If so, concatenate the values of the new item with what's already in the dictionary
            for key, value in block.items():
                if key in spimi_index.keys():
                    spimi_index[key].update(value)
                else:
                    spimi_index[key] = value

    return spimi_index

# ===============SINGLE QUERY==================

def singleQuery(queryInput):
    spimi_index = read_spimi_index()

    # normalize the user query
    if len(queryInput.strip().split()) == 1:
        print('--- Single Keyword Query')
        single_keyword = queryInput.strip().split()[0]
        single_keyword_normalized = preprocessing.normalize([single_keyword])
        keyword = single_keyword_normalized[0]

        bm25_scores = dict()

        # check if single keyword exists in spimi_index keys
        if keyword in spimi_index.keys():
            matches = spimi_index[keyword]
            doc_freq = len(matches.keys())

            for doc_id, term_freq in matches.items():
                query_parameters = {
                    keyword: {
                        'doc_freq': doc_freq,
                        'term_freq': term_freq,
                        'doc_id': doc_id
                    }
                }

                # calculate the bm25 score for each document
                bm25_scores[doc_id] = bm25Score.calculate_score(query_parameters, k1, b)
                sorted_scores = sorted(bm25_scores.items(), key=operator.itemgetter(1), reverse=True)

            print('Matches: ', sorted_scores)
        else:
            print('No documents found!')

# ===============INTERSECTION==================

def multiAndQuery(queryInput):
    spimi_index = read_spimi_index()
    union_list = []
    scores = dict()

    # normalize the user query
    query_terms = queryInput.strip().replace(" ", "").split("&&")
    print('--- Multiple Keyword Query')
    terms = preprocessing.normalize(query_terms)
    print('--- Terms:', query_terms)

    # append postings lists for each term to union_list
    for term in terms:
        union_list.extend(spimi_index[term])

    # find duplicate items in union list
    doc_id_intersection = [item for item, count in collections.Counter(union_list).items() if count == len(terms)]

    doc_freq = len(doc_id_intersection)

    for term in terms:
        for doc_id in doc_id_intersection:
            query_parameters = {
                term: {
                    'doc_freq': doc_freq,
                    'term_freq': spimi_index[term][doc_id],
                    'doc_id': doc_id
                }
            }

            # calculate the bm25 score for each document
            scores[doc_id] = bm25Score.calculate_score(query_parameters, k1, b)
            sorted_scores = sorted(scores.items(), key=operator.itemgetter(1), reverse=True)

    if (len(doc_id_intersection) == 0):
        print("No documents found")
    else:
        print('Matches: ', sorted_scores)


# ===============UNION==================

def multiOrQuery(queryInput):
    spimi_index = read_spimi_index()
    union_list = []
    scores = dict()

    # normalize the user query
    query_terms = queryInput.strip().replace(" ", "").split("||")
    print('--- Multiple Keyword Query')
    terms = preprocessing.normalize(query_terms)
    print('--- Terms:', query_terms)

    # append postings lists for each term to union_list
    for term in terms:
        union_list.extend(spimi_index[term].keys())

    # return the set of union_list (no duplicates) as a list
    doc_id_union = list(set(union_list))

    doc_freq = len(doc_id_union)

    for term in terms:
        for doc_id in doc_id_union:
            # Ensure term frequency is zero, if it is not in this document
            if doc_id in spimi_index[term]:
                term_freq = spimi_index[term][doc_id]
            else:
                term_freq = 0

            query_parameters = {
                term: {
                    'doc_freq': doc_freq,
                    'term_freq': term_freq,
                    'doc_id': doc_id
                }
            }

            # calculate the bm25 score for each document
            scores[doc_id] = bm25Score.calculate_score(query_parameters, k1, b)
            sorted_scores = sorted(scores.items(), key=operator.itemgetter(1), reverse=True)

    if (len(doc_id_union) == 0):
        print("No documents found")
    else:
        print('Matches: ', sorted_scores)


# ===============MAIN METHOD==================

if __name__ == '__main__':
    print("======== QUERY GENERATOR ========")
    print("1. Single Keyword Query")
    print("2. Multiple Keywords AND Query")
    print("3. Multiple Keywords OR Query"+"\n")

    queryInput = input("Please choose a number (1, 2, or 3) from the list above: ")

    if queryInput == '1':
        qi = input("Please type your single keyword query: ")
        singleQuery(qi)
    elif queryInput == '2':
        qi = input("Please type your multi keywords AND query: ")
        multiAndQuery(qi)
    elif queryInput == '3':
        qi = input("Please type your multi keyword OR query: ")
        multiOrQuery(qi)
    else:
        print("Incorrect Query.")




