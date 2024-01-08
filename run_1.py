import read_data
from configs import *

from collections import Counter, defaultdict
from itertools import islice
import math
import numpy as np

from nltk import download
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet


def get_freq_dictionary(docs_collection: dict):
    print("freq dict calculation...")
    coll_term_list = []
    for terms in docs_collection.values():
        coll_term_list += terms
    collection_freq_dict = Counter(coll_term_list)
    return collection_freq_dict


def remove_stop_words(docs_collection: dict, stop_list):
    print("stop-words removing...")
    coll_length = len(docs_collection)
    for k, docno in enumerate(docs_collection):
        if k % 10000 == 0:
            print(k, "of", coll_length, "docs")

        docs_collection[docno] = [term for term in docs_collection[docno] if term not in stop_list]

        # clean_terms = docs_collection[docno]
        # for i, term in enumerate(docs_collection[docno]):
        #     if term in stop_list:
        #         clean_terms.remove(term)
        # docs_collection[docno] = clean_terms

    return docs_collection


def nltk_lemmatizer(docs_collection: dict):
    print("nltk lemmatization...")
    download('wordnet')
    download('punkt')
    lemmatizer = WordNetLemmatizer()

    coll_length = len(docs_collection)
    for k, docno in enumerate(docs_collection):
        if k % 10000 == 0:
            print(k, "of", coll_length, "docs")
        for i, term in enumerate(docs_collection[docno]):
            docs_collection[docno][i] = lemmatizer.lemmatize(term)
    return docs_collection


def manual_lemmatizer(docs_collection: dict):
    print("manual lemmatization...")
    for docno in docs_collection:
        for i, term in enumerate(docs_collection[docno]):
            tl = len(term)
            stop_words_set = set(CZ_LOW_IDF_500)
            if term not in stop_words_set:
                if tl == 4:
                    rt = term[:-1]
                if tl == 5:
                    rt = term[:-1]
                elif tl == 6:
                    rt = term[:-1]
                elif tl == 7:
                    rt = term[:-2]
                elif tl == 8:
                    rt = term[:-2]
                elif tl == 9:
                    rt = term[:-2]
                elif tl == 10:
                    rt = term[:-2]
                elif tl == 11:
                    rt = term[:-3]
                elif tl > 11:
                    rt = term[:-3]
                else:
                    rt = term
                docs_collection[docno][i] = rt
    return docs_collection


def get_freq_dictionary_reduced(docs_collection: dict):
    print("reduced freq dict calculation...")
    coll_term_list = []
    for terms in docs_collection.values():
        coll_term_list += terms
    collection_freq_dict = Counter(coll_term_list)

    reduced_terms = {}
    for term in collection_freq_dict.keys():
        tl = len(term)
        if tl == 6:
            rt = term[:-1]
        elif tl == 7:
            rt = term[:-2]
        elif tl == 8:
            rt = term[:-2]
        elif tl == 9:
            rt = term[:-2]
        elif tl == 10:
            rt = term[:-3]
        elif tl == 11:
            rt = term[:-4]
        elif tl > 11:
            rt = term[:-3]
        else:
            rt = term
        reduced_terms[rt] = reduced_terms.get(rt, 0) + collection_freq_dict[term]

    return collection_freq_dict


def expand_query(docs_collection: dict, terms_idf: dict, syn_group_size=5):
    print("query expansion...")
    download('wordnet')
    for docno in docs_collection:
        expansion = {}
        for term in docs_collection[docno]["terms_list"]:
            if term not in terms_idf or terms_idf[term] > 0.5:
                synonyms = set()
                synonyms.add(term)
                for syn in wordnet.synsets(term):
                    if len(synonyms) < syn_group_size-1:
                        for sm in syn.lemmas():
                            sms = sm.name().split("_")
                            if len(sms) == 1:
                                for s in sms:
                                    if s in terms_idf.keys() and terms_idf[s] > 0.5 and len(synonyms) < syn_group_size:
                                        synonyms.add(s)
                expansion[term] = list(synonyms)
        docs_collection[docno]["expansion"] = expansion

    return docs_collection


def calc_tf(docs_collection: dict):
    print("tf calculation...")
    docs_upd = {}
    counter = 0
    for docno, terms in docs_collection.items():
        counter += 1
        doc_freq_dict = Counter(terms)
        docs_upd[docno] = {"terms_list": terms, "tf": doc_freq_dict}
    return docs_upd


def calc_log_tf(docs_collection: dict):
    print("tf log calculation...")
    docs_upd = {}
    for docno, terms in docs_collection.items():
        doc_freq_dict = Counter(terms)
        doc_tf = {term: (1 + math.log(tf, 10)) for term, tf in doc_freq_dict.items()}
        docs_upd[docno] = {"terms_list": terms, "tf": doc_tf}
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


def calc_tf_idf(docs_collection: dict, idf: dict):
    print("tf-idf calculation...")
    n = len(docs_collection)
    for docno in docs_collection:
        tf_idf = {}
        for term, tf in docs_collection[docno]["tf"].items():
            if term in idf.keys():
                tf_idf[term] = tf*idf[term]
            else:
                tf_idf[term] = tf * 1
        docs_collection[docno]["tf-idf"] = tf_idf
    return docs_collection


def calc_vector_tf(docs_collection: dict):
    print("vectors calculation...")
    # to check the progress
    coll_length = len(docs_collection)
    for i, docno in enumerate(docs_collection):
        # to check the progress
        if i % 10000 == 0:
            print(i, "of", coll_length, 'docs')

        doc_tf = docs_collection[docno]["tf"]
        keys = list(doc_tf.keys())
        values = np.array(list(doc_tf.values()))

        denom = np.sqrt(np.sum(values**2))
        doc_vec_values = values / denom
        doc_vec = {tf_key: doc_vec_value for (tf_key, doc_vec_value) in zip(keys, doc_vec_values)}
        docs_collection[docno]["vector"] = doc_vec
    return docs_collection


def calc_vector_tf_idf(docs_collection: dict):
    print("vectors calculation...")
    # to check the progress
    coll_length = len(docs_collection)
    for i, docno in enumerate(docs_collection):
        # to check the progress
        if i % 10000 == 0:
            print(i, "of", coll_length, 'docs')

        doc_tf = docs_collection[docno]["tf-idf"]
        keys = list(doc_tf.keys())
        values = np.array(list(doc_tf.values()))

        denom = np.sqrt(np.sum(values**2))
        doc_vec_values = values / denom
        doc_vec = {tf_key: doc_vec_value for (tf_key, doc_vec_value) in zip(keys, doc_vec_values)}
        docs_collection[docno]["vector"] = doc_vec
    return docs_collection


def calc_similarity(docs_vec: dict, topics_vec: dict, idf, top_rank=100):
    print("similarity calculation...")
    topic_sim = {}
    for topic in topics_vec:
        rare_terms = [term for term in topics_vec[topic]["vector"] if (term not in idf.keys()) or (idf[term] > 0.8)]
        for doc in docs_vec:
            sim = 0
            for term in rare_terms:
                if term in docs_vec[doc]["vector"]:
                    sim += topics_vec[topic]["vector"][term]*docs_vec[doc]["vector"][term]
            topic_sim[doc] = round(sim, 5)
        sim_sorted = dict(sorted(topic_sim.items(), key=lambda item: item[1], reverse=True))
        sim_top_rank = dict(islice(sim_sorted.items(), top_rank))
        topics_vec[topic]["similarity"] = sim_top_rank
    return topics_vec


def calc_similarity_expanded(docs_vec: dict, topics_vec: dict, idf, top_rank=100):
    print("expanded queries similarity calculation...")
    topic_sim = {}
    for topic in topics_vec:
        rare_terms = [term for term in topics_vec[topic]["vector"] if (term not in idf.keys()) or (idf[term] > 0.5)]
        for doc in docs_vec:
            sim = 0

            check_flag = True
            avg_term_tf = 1
            for term in rare_terms:
                avg_term_tf = topics_vec[topic]["vector"][term]
                doc_terms = list(docs_vec[doc]["vector"].keys())
                flag = any(word in doc_terms for word in topics_vec[topic]['expansion'][term])
                if not flag:
                    check_flag = False
                    break

            if check_flag:
                ext_query = []
                for synonyms in topics_vec[topic]['expansion'].values():
                    ext_query.extend(synonyms)
                for term in ext_query:
                    if term in docs_vec[doc]["vector"].keys():
                        sim += avg_term_tf*docs_vec[doc]["vector"][term]

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
            print("\nrun-1 cz train")
            topics_file = CZ_CLEAN_TOPICS_FILE_PATH
            save_to = CZ_TRAIN_RESULTS_PATH_RUN1
        else:
            print("\nrun-1 cz test")
            topics_file = CZ_CLEAN_TEST_TOPICS_FILE_PATH
            save_to = CZ_TEST_RESULTS_PATH_RUN1

        # BEST CZECH
        print("docs downloading...")
        docs = read_data.get_docs(CZ_CLEAN_DOCS_FILE_PATH)
        print("topics downloading...")
        topics = read_data.get_topics(topics_file)

        reduced_docs = manual_lemmatizer(docs)
        reduced_topics = manual_lemmatizer(topics)

        docs_tf = calc_log_tf(reduced_docs)
        terms_idf = calc_idf(reduced_docs)
        docs_tf_idf = calc_tf_idf(docs_tf, terms_idf)
        docs_vec = calc_vector_tf_idf(docs_tf_idf)

        topics_tf = calc_log_tf(reduced_topics)
        topics_tf_idf = calc_tf_idf(topics_tf, terms_idf)
        topics_vec = calc_vector_tf_idf(topics_tf_idf)
        topics_sim = calc_similarity(docs_vec, topics_vec, terms_idf, 1000)

        save_results_to_file(topics_sim, "run_1", save_to)
    if lang == EN:
        if train_test == "train":
            print("\nrun-1 en train")
            topics_file = EN_CLEAN_TOPICS_FILE_PATH
            save_to = EN_TRAIN_RESULTS_PATH_RUN1
        else:
            print("\nrun-1 en test")
            topics_file = EN_CLEAN_TEST_TOPICS_FILE_PATH
            save_to = EN_TEST_RESULTS_PATH_RUN1

        # BEST ENGLISH
        print("docs downloading...")
        docs = read_data.get_docs(EN_CLEAN_DOCS_FILE_PATH)
        print("topics downloading...")
        topics = read_data.get_topics(topics_file)

        # raw tf and all rare words
        lemm_docs = nltk_lemmatizer(docs)
        lemm_docs = remove_stop_words(lemm_docs, EN_LOW_IDF_LEMM_300)

        lemm_topics = nltk_lemmatizer(topics)
        lemm_topics = remove_stop_words(lemm_topics, EN_LOW_IDF_LEMM_300)

        docs_tf = calc_tf(lemm_docs)
        terms_idf = calc_idf(lemm_docs)
        docs_vec = calc_vector_tf(docs_tf)

        topics_tf = calc_tf(lemm_topics)
        topics_exp = expand_query(topics_tf, terms_idf, 6)

        topics_vec = calc_vector_tf(topics_exp)
        topics_sim = calc_similarity_expanded(docs_vec, topics_vec, terms_idf, 1000)

        save_results_to_file(topics_sim, "run_1", save_to)
