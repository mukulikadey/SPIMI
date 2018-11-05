
from collections import OrderedDict
import os
import json

class SPIMI:
    def __init__(self, block_size_limit, documents):
        self.block_size_limit = block_size_limit
        self.documents = documents

    def invert(self):
        index_number = 0
        block_number = 0
        dictionary = {}

        for docId in self.documents.keys():
            index_number += 1

            for token in self.documents[docId]:
                if token not in dictionary:
                    postings_list = self.add_to_dictionary(dictionary, token)
                else:
                    postings_list = self.get_postings_list(dictionary, token)

                # calculating the term frequency
                if docId not in postings_list.keys():
                    # if docID is encountered for the first time, we set the frequency counter to 1
                    postings_list[docId] = 1
                else:
                    # if docId is encountered again, we increment our frequency counter
                    postings_list[docId] += 1


            # Checks if the block has reached the max number of articles, set by block_size_max
            if index_number >= self.block_size_limit:
                sorted_dictionary = sort_terms(dictionary)
                write_block_to_disk(sorted_dictionary, block_number)

                block_number += 1
                index_number = 0
                dictionary = {}

        sorted_dictionary = sort_terms(dictionary)
        write_block_to_disk(sorted_dictionary, block_number)

    def add_to_dictionary(self, dictionary, token):
        dictionary[token] = {}
        return dictionary[token]

    def get_postings_list(self, dictionary, token):
        return dictionary[token]


def sort_terms(dictionary):
    sorted_dictionary = OrderedDict()
    sorted_terms = sorted(dictionary)  # Sorts the dictionary alphabetically by terms

    for term in sorted_terms:
        old_postings_list = dictionary[term]
        new_postings_list = old_postings_list

        sorted_dictionary[term] = new_postings_list

    return sorted_dictionary


def write_block_to_disk(sorted_dictionary, block_number):
    block_path_parts = ['DISK/', 'BLOCK', str(block_number).zfill(3), '.txt']
    block_path = ''.join(block_path_parts)

    if not os.path.exists('DISK/'):
        os.makedirs('DISK/')

    with open(block_path, 'w') as f:
        json.dump(sorted_dictionary, f)
