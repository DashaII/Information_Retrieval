import read_data
from configs import *

from collections import Counter, defaultdict
from itertools import islice
import math
import numpy as np


def get_freq_dictionary(docs_collection: dict):
    print("freq dict calculation...")
    coll_term_list = []
    for terms in docs_collection.values():
        coll_term_list += terms
    collection_freq_dict = Counter(coll_term_list)
    return collection_freq_dict


def calc_tf(docs_collection: dict):
    print("tf calculation...")
    docs_upd = {}
    counter = 0
    for docno, terms in docs_collection.items():
        counter += 1
        doc_freq_dict = Counter(terms)
        docs_upd[docno] = {"terms_list": terms, "tf": doc_freq_dict}
    return docs_upd


def calc_df(docs_collection: dict):
    print("df calculation...")
    df = defaultdict(int)
    for terms in docs_collection.values():
        term_set = set(terms)
        for term in term_set:
            df[term] += 1
    return df


def calc_idf(docs_collection: dict):
    print("idf calculation...")
    df = calc_df(docs_collection)
    n = len(docs_collection)
    idf = {term: math.log(n/df[term], 10) for term in df}
    idf = dict(sorted(idf.items(), key=lambda item: item[1]))
    return idf


def calc_vector(docs_collection: dict):
    print("vectors calculation...")
    # to check the progress
    coll_length = len(docs_collection)
    for i, docno in enumerate(docs_collection):
        # to check the progress
        if i % 10000 == 0:
            print(i, "of", coll_length)

        doc_tf = docs_collection[docno]["tf"]
        tf_keys = list(doc_tf.keys())
        tf_values = np.array(list(doc_tf.values()))

        denom = np.sqrt(np.sum(tf_values**2))
        doc_vec_values = tf_values / denom
        doc_vec = {tf_key: doc_vec_value for (tf_key, doc_vec_value) in zip(tf_keys, doc_vec_values)}
        docs_collection[docno]["vector"] = doc_vec
    return docs_collection


def calc_similarity(docs_vec: dict, topics_vec: dict, top_rank=100):
    print("similarity calculation...")
    topic_sim = {}
    for topic in topics_vec:
        for doc in docs_vec:
            sim = 0
            for term in topics_vec[topic]["vector"]:
                if term in docs_vec[doc]["vector"]:
                    sim += topics_vec[topic]["vector"][term]*docs_vec[doc]["vector"][term]
            topic_sim[doc] = round(sim, 5)
        sim_sorted = dict(sorted(topic_sim.items(), key=lambda item: item[1], reverse=True))
        sim_top_rank = dict(islice(sim_sorted.items(), top_rank))
        topics_vec[topic]["similarity"] = sim_top_rank
    return topics_vec


def save_results_to_file(topics_sim: dict, run: str, file_name: str):
    print("results saving...")
    with open(file_name, 'w', encoding='utf-8') as f:
        for topic in topics_sim:
            rank = 0
            for doc, sim in topics_sim[topic]["similarity"].items():
                f.write(f"{topic} 0 {doc} {rank} {sim} {run}\n")
                rank += 1


def run(lang, train_test):
    if lang == CZ:
        if train_test == "train":
            print("\nrun-0 cz train")
            topics_file = CZ_CLEAN_TOPICS_FILE_PATH
            save_to = CZ_TRAIN_RESULTS_PATH_RUN0
        else:
            print("\nrun-0 cz test")
            topics_file = CZ_CLEAN_TEST_TOPICS_FILE_PATH
            save_to = CZ_TEST_RESULTS_PATH_RUN0

        # CZ
        print("docs downloading...")
        docs = read_data.get_docs(CZ_CLEAN_DOCS_FILE_PATH)
        print("topics downloading...")
        topics = read_data.get_topics(topics_file)

        docs_tf = calc_tf(docs)
        docs_vec = calc_vector(docs_tf)

        topics_tf = calc_tf(topics)
        topics_vec = calc_vector(topics_tf)
        topics_sim = calc_similarity(docs_vec, topics_vec, 1000)

        save_results_to_file(topics_sim, "run_0", save_to)
    elif lang == EN:
        if train_test == "train":
            print("\nrun-0 en train")
            topics_file = EN_CLEAN_TOPICS_FILE_PATH
            save_to = EN_TRAIN_RESULTS_PATH_RUN0
        else:
            print("\nrun-0 en test")
            topics_file = EN_CLEAN_TEST_TOPICS_FILE_PATH
            save_to = EN_TEST_RESULTS_PATH_RUN0

        # EN
        print("docs downloading...")
        docs = read_data.get_docs(EN_CLEAN_DOCS_FILE_PATH)
        print("topics downloading...")
        topics = read_data.get_topics(topics_file)

        docs_tf = calc_tf(docs)
        docs_vec = calc_vector(docs_tf)

        topics_tf = calc_tf(topics)
        topics_vec = calc_vector(topics_tf)
        topics_sim = calc_similarity(docs_vec, topics_vec, 1000)

        save_results_to_file(topics_sim, "run_0", save_to)
