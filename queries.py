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
            index.update(block_object)

    return index

# ===============SINGLE QUERY==================

def singleQuery(queryInput):
    spimi_index = read_spimi_index()
    print('SPIMI INDEX: ',spimi_index)
    if len(queryInput.strip().split()) == 1:
        print('--- Single Keyword Query')
        single_keyword = queryInput.strip().split()[0]
        single_keyword_normalized = preprocessing.normalize([single_keyword])
        keyword = single_keyword_normalized[0]

        scores = {}

        if keyword in spimi_index:
            hits = spimi_index[keyword]

            dft = len(hits.keys())

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
            print('Hits: ', sorted_scores)
        else:
            print('No documents found!')

# ===============INTERSECTION==================

def intersect(a, b):
    return a.intersection(b)

def multiAndQuery(queryInput):
    spimi_index = read_spimi_index()
    tmpDict = {}
    tmpList = []
    union_list = []

    query_terms = queryInput.strip().replace(" ", "").split("and")
    print('--- Multiple Keyword Query')
    terms = preprocessing.normalize(query_terms)
    print('--- Terms:', query_terms)

    # add to temp dict
    for term in terms:
        if term in spimi_index.keys():
            tmpDict[term] = spimi_index[term]
        else:
            tmpDict[term] = []

    # add to temp list
    for key, value in tmpDict.items():
        tmpList.append(value)

    # add to union list
    for i in range(len(tmpList)):
        for j in range(len(tmpList[i])):
            union_list.append(tmpList[i][j])

    # find duplicate items in union list
    dup_items = [item for item, count in collections.Counter(union_list).items() if count > 1]

    if (len(dup_items) == 0):
        print("No documents found")
    else:
        print("Intersecting PL: ", dup_items)


# ===============UNION==================

def multiOrQuery(queryInput):
    spimi_index = read_spimi_index()
    tmpDict = {}
    tmpList = []
    union_list = []

    query_terms = queryInput.strip().replace(" ", "").split("or")
    print('--- Multiple Keyword Query')
    terms = preprocessing.normalize(query_terms)
    print('--- Terms:', query_terms)

    # add to temp dict
    for term in terms:
        if term in spimi_index.keys():
            tmpDict[term] = spimi_index[term]

        else:
            tmpDict[term] = []

    # add to temp list
    for key, value in tmpDict.items():
        tmpList.append(value)

    # add to union list
    for i in range(len(tmpList)):
        for j in range(len(tmpList[i])):
            union_list.append(tmpList[i][j])

    # remove duplicates from union list
    result = remove_duplicates(union_list)

    if (len(result) == 0):
        print("No documents found")
    else:
        print("Union PL: ", result)

def remove_duplicates(values):
    output = []
    seen = set()
    for value in values:
        # If value has not been encountered yet,
        # ... add it to both list and set.
        if value not in seen:
            output.append(value)
            seen.add(value)
    return output

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




