import preprocessing
import reuters
from glob import iglob
from collections import OrderedDict
import ast
import collections
import itertools
import re
import json
import bm25Score
import operator
import functools
import os

k1 = 1.5
b = 0.8

# ===============READ SPIMI INDEX==================

def read_spimi_index():
    index = OrderedDict()
    files_paths = []

    for file_path in iglob('DISK/BLOCK*.txt'):
        files_paths.append(file_path)

    for file in files_paths:
        with open(file, 'r') as file:
            block_object = json.load(file)

            # Check if any of these items were already added to the index
            # If so, concatenate the values of the new item with what's already in the dict
            for key, value in block_object.items():
                if key in index.keys():
                    index[key].update(value)
                else:
                    index[key] = value

    return index

# ===============SINGLE QUERY==================

def singleQuery(queryInput):
    spimi_index = read_spimi_index()

    if len(queryInput.strip().split()) == 1:
        print('--- Single Keyword Query')
        single_keyword = queryInput.strip().split()[0]
        single_keyword_normalized = preprocessing.normalize([single_keyword])
        keyword = single_keyword_normalized[0]

        scores = {}

        if keyword in spimi_index.keys():
            hits = spimi_index[keyword]

            dft = len(hits.keys()) # document frequency

            for docid, tftd in hits.items():
                query_parameters = {
                    keyword: {
                        'dft': dft,
                        'tftd': tftd,
                        'docid': docid
                    }
                }

                scores[docid] = bm25Score.get_score(query_parameters, k1, b)
                sorted_scores = sorted(scores.items(), key=operator.itemgetter(1), reverse=True)

            print('Number of hits: ', len(scores.keys()))
            print('Matches: ', hits)
            print('Scores: ', sorted_scores)
        else:
            print('No documents found!')

# ===============INTERSECTION==================

def multiAndQuery(queryInput):
    spimi_index = read_spimi_index()
    tmpDict = {}
    tmpList = []
    union_list = []

    query_terms = queryInput.strip().replace(" ", "").split("&&")
    print('--- Multiple Keyword Query')
    terms = preprocessing.normalize(query_terms)
    print('--- Terms:', query_terms)

    # add to temp dict
    for term in terms:
        union_list.extend(spimi_index[term])

    # find duplicate items in union list
    doc_id_intersection = [item for item, count in collections.Counter(union_list).items() if count == len(terms)]

    doc_freq = len(doc_id_intersection)
    scores = dict()
    for term in terms:
        for docid in doc_id_intersection:
            query_parameters = {
                term: {
                    'dft': doc_freq,
                    'tftd': spimi_index[term][docid],
                    'docid': docid
                }
            }

            scores[docid] = bm25Score.get_score(query_parameters, k1, b)
            sorted_scores = sorted(scores.items(), key=operator.itemgetter(1), reverse=True)

    if (len(doc_id_intersection) == 0):
        print("No documents found")
    else:
        print('Number of hits: ', len(scores.keys()))
        print('Matches: ', doc_id_intersection)
        print('Scores: ', sorted_scores)


# ===============UNION==================

def multiOrQuery(queryInput):
    spimi_index = read_spimi_index()
    tmpDict = {}
    tmpList = []
    union_list = []

    query_terms = queryInput.strip().replace(" ", "").split("||")
    print('--- Multiple Keyword Query')
    terms = preprocessing.normalize(query_terms)
    print('--- Terms:', query_terms)

    # add to temp dict
    for term in terms:
        union_list.extend(spimi_index[term].keys())

    # find duplicate items in union list
    doc_id_union = list(set(union_list))

    doc_freq = len(doc_id_union)
    scores = dict()
    for term in terms:
        for docid in doc_id_union:
            # Ensure term frequency is zero, if it is not in this document
            if docid in spimi_index[term]:
                tftd = spimi_index[term][docid]
            else:
                tftd = 0

            query_parameters = {
                term: {
                    'dft': doc_freq,
                    'tftd': tftd,
                    'docid': docid
                }
            }

            scores[docid] = bm25Score.get_score(query_parameters, k1, b)
            sorted_scores = sorted(scores.items(), key=operator.itemgetter(1), reverse=True)

    if (len(doc_id_union) == 0):
        print("No documents found")
    else:
        print('Number of hits: ', len(scores.keys()))
        print('Matches: ', doc_id_union)
        print('Scores: ', sorted_scores)


def remove_duplicates(values):
    val_set=set(values)

    return list(val_set)
    # output = []
    # seen = set()
    # for value in values:
    #     # If value has not been encountered yet,
    #     # ... add it to both list and set.
    #     if value not in seen:
    #         output.append(value)
    #         seen.add(value)
    # return output

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




