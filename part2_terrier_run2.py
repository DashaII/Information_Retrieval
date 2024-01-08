import my_czech_stemmer
import parse_data
from configs import *
from functions import *
import read_data
import os
import pandas as pd
import pyterrier as pt
import czech_stemmer
if not pt.started():
    pt.init()


def run_2(lang, train_test, run_no, index_path, save_to_path, qrels_path):
    if lang == EN:
        docs_file = EN_CLEAN_DOCS_FILE_PATH
        if train_test == TRAIN:
            print("\n", run_no, lang, train_test)
            topics_file = EN_CLEAN_TOPICS_FILE_PATH
        else:
            print("\n", run_no, lang, train_test)
            topics_file = EN_CLEAN_TEST_TOPICS_FILE_PATH

    if lang == CZ:
        docs_file = CZ_CLEAN_DOCS_FILE_PATH
        if train_test == TRAIN:
            print("\n", run_no, lang, train_test)
            topics_file = CZ_CLEAN_TOPICS_FILE_PATH
        else:
            print("\n", run_no, lang, train_test)
            topics_file = CZ_CLEAN_TEST_TOPICS_FILE_PATH

    # download docs and topics
    print("docs downloading...")
    docs = read_data.get_docs(docs_file)
    print("topics downloading...")
    topics = read_data.get_topics(topics_file)

    # apply stemmer for czech lang
    if lang == CZ:
        docs = cz_stemmer(docs)
        topics = cz_stemmer(topics)

        stopwords = []
        for word in CZ_LOW_IDF_500:
            stopwords.append(czech_stemmer.cz_stem_word(word))
        print("stopwords removal...")
        conv_docs = {k: ' '.join(v for v in docs[k] if v not in stopwords[:180]) for k in docs}
        conv_topics = {k: ' '.join(v for v in topics[k] if v not in stopwords[:180]) for k in topics}

    if lang == EN:
        # convert docs and topics dictionaries to 1-string format
        conv_docs = {k: ' '.join(v) for k, v in docs.items()}
        conv_topics = {k: ' '.join(v) for k, v in topics.items()}

    # convert docs and topics to DataFrames
    docs_df = pd.DataFrame({'docno': list(conv_docs.keys()), 'text': list(conv_docs.values())})
    topics_df = pd.DataFrame({'qid': list(conv_topics.keys()), 'query': list(conv_topics.values())})

    print("create indexer...")
    if os.path.exists(index_path) and os.listdir(index_path):
        index_ref = pt.IndexFactory.of(index_path)
    else:
        if lang == CZ:
            indexer = pt.DFIndexer(index_path, stemmer=None, stopwords=None, tokeniser="UTFTokeniser", verbose=True)
        elif lang == EN:
            indexer = pt.DFIndexer(index_path, verbose=True)
        index_ref = indexer.index(docs_df["text"], docs_df["docno"])

    # retrieve documents for queries
    print("retrieve documents for queries...")
    if lang == EN:
        retr = pt.BatchRetrieve(index_ref, controls={"wmodel": "LemurTF_IDF"}, verbose=True)
    elif lang == CZ:
        retr = pt.BatchRetrieve(index_ref, controls={"wmodel": "IFB2"}, verbose=True)

    print("transform...")
    res = retr.transform(topics_df)

    save_results_to_file(res, run_no, save_to_path)
    evaluate(res, qrels_path)


if __name__ == '__main__':
    # parse full docs and topics files
    parse_data.parse_full_data_run_2()

    run_2(CZ, TRAIN, RUN2, CZ_INDEX_PATH_RUN2, TER_CZ_TRAIN_RESULTS_PATH_RUN2, CZ_QRELS)
    run_2(CZ, TEST, RUN2, CZ_INDEX_PATH_RUN2, TER_CZ_TEST_RESULTS_PATH_RUN2, CZ_QRELS)

    run_2(EN, TRAIN, RUN2, EN_INDEX_PATH_RUN2, TER_EN_TRAIN_RESULTS_PATH_RUN2, EN_QRELS)
    run_2(EN, TEST, RUN2, EN_INDEX_PATH_RUN2, TER_EN_TEST_RESULTS_PATH_RUN2, EN_QRELS)

