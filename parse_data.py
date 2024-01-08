import xml.etree.ElementTree as ET
import re
import json
from configs import *


def read_file(fine_name):
    with open(fine_name, 'r', encoding='utf-8') as file:
        text = file.read()
    return text


def read_list_from_file(fine_name):
    with open(fine_name, 'r', encoding='utf-8') as file:
        doc_list = file.readlines()
    return doc_list


def parsexml(filename, docs, tags_list, item_tag, itemid_tag):
    tree = ET.parse(filename)
    root = tree.getroot()

    for doc in root.iter(item_tag):
        docno = ""
        for child in doc:
            if child.tag == itemid_tag:
                docno = child.text
                docs[child.text] = ""
            if child.tag in tags_list:
                if child.text is not None:
                    docs[docno] += " " + child.text

    return docs


def parsexml_list(folder_path, tags_list, item_tag, itemid_tag, xmllist):
    docs = {}
    for xml_name in xmllist:
        parsexml(folder_path + "/" + xml_name, docs, tags_list, item_tag, itemid_tag)
    return docs


def clean_data(data_dict: dict, separators, run0: bool):
    for key, value in data_dict.items():
        if run0:
            text_split = re.split(separators, value)
        else:
            text_split = re.split(separators, value.lower())
        # exclude empty strings
        text_split = [item for item in text_split if item]
        data_dict[key] = text_split
    return data_dict


def save_to_json(data_dict, file_name):
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(data_dict, f, ensure_ascii=False)


# parse documents and topics
# clean documents and topics
# save documents and topics to json
def parse_full_data_run_0():
    # CZ docs
    print("parsing cz docs...")
    doc_list_cz = read_file(CZ_DOCS_FULL_LIST_PATH).split()
    docs_cz = parsexml_list(CZ_DOCS_FOLDER_PATH, CZ_TAGS, DOC_TAG, DOCNO_TAG, doc_list_cz)
    clean_docs_cz = clean_data(docs_cz, CZ_SEPARATORS_RUN0, 1)
    save_to_json(clean_docs_cz, CZ_CLEAN_DOCS_FILE_PATH)

    # CZ topics
    print("parsing cz train topics...")
    topics_cz = {}
    topics_cz = parsexml(CZ_TRAIN_TOPICS_PATH, topics_cz, TOPIC_TITLE_TAG, TOPIC_TAG, TOPIC_NUM_TAG)
    clean_topics_cz = clean_data(topics_cz, CZ_SEPARATORS_RUN0, 1)
    save_to_json(clean_topics_cz, CZ_CLEAN_TOPICS_FILE_PATH)

    # CZ test topics
    print("parsing cz test topics...")
    topics_test_cz = {}
    topics_test_cz = parsexml(CZ_TEST_TOPICS_PATH, topics_test_cz, TOPIC_TITLE_TAG, TOPIC_TAG, TOPIC_NUM_TAG)
    clean_topics_cz = clean_data(topics_test_cz, CZ_SEPARATORS_RUN0, 1)
    save_to_json(clean_topics_cz, CZ_CLEAN_TEST_TOPICS_FILE_PATH)

    # EN docs
    print("parsing en docs...")
    doc_list_en = read_file(EN_DOCS_FULL_LIST_PATH).split()
    docs_en = parsexml_list(EN_DOCS_FOLDER_PATH, EN_TAGS, DOC_TAG, DOCNO_TAG, doc_list_en)
    clean_docs_en = clean_data(docs_en, EN_SEPARATORS_RUN0, 1)
    save_to_json(clean_docs_en, EN_CLEAN_DOCS_FILE_PATH)

    # EN topics
    print("parsing en train topics...")
    topics_en = {}
    topics_en = parsexml(EN_TRAIN_TOPICS_PATH, topics_en, TOPIC_TITLE_TAG, TOPIC_TAG, TOPIC_NUM_TAG)
    clean_topics_en = clean_data(topics_en, EN_SEPARATORS_RUN0,1)
    save_to_json(clean_topics_en, EN_CLEAN_TOPICS_FILE_PATH)

    # EN test topics
    print("parsing en test topics...")
    topics_test_en = {}
    topics_test_en = parsexml(EN_TEST_TOPICS_PATH, topics_test_en, TOPIC_TITLE_TAG, TOPIC_TAG, TOPIC_NUM_TAG)
    clean_topics_en = clean_data(topics_test_en, EN_SEPARATORS_RUN0, 1)
    save_to_json(clean_topics_en, EN_CLEAN_TEST_TOPICS_FILE_PATH)


def parse_full_data_run_1():
    # CZ docs
    print("parsing cz docs...")
    doc_list_cz = read_file(CZ_DOCS_FULL_LIST_PATH).split()
    docs_cz = parsexml_list(CZ_DOCS_FOLDER_PATH, CZ_TAGS, DOC_TAG, DOCNO_TAG, doc_list_cz)
    clean_docs_cz = clean_data(docs_cz, CZ_SEPARATORS_RUN1, 0)
    save_to_json(clean_docs_cz, CZ_CLEAN_DOCS_FILE_PATH)

    # CZ train topics
    print("parsing cz train topics...")
    topics_train_cz = {}
    topics_train_cz = parsexml(CZ_TRAIN_TOPICS_PATH, topics_train_cz, TOPIC_TITLE_TAG, TOPIC_TAG, TOPIC_NUM_TAG)
    clean_topics_cz = clean_data(topics_train_cz, CZ_SEPARATORS_RUN1, 0)
    save_to_json(clean_topics_cz, CZ_CLEAN_TOPICS_FILE_PATH)

    # CZ test topics
    print("parsing cz test topics...")
    topics_test_cz = {}
    topics_test_cz = parsexml(CZ_TEST_TOPICS_PATH, topics_test_cz, TOPIC_TITLE_TAG, TOPIC_TAG, TOPIC_NUM_TAG)
    clean_topics_cz = clean_data(topics_test_cz, CZ_SEPARATORS_RUN1, 0)
    save_to_json(clean_topics_cz, CZ_CLEAN_TEST_TOPICS_FILE_PATH)

    # EN docs
    print("parsing en docs...")
    doc_list_en = read_file(EN_DOCS_FULL_LIST_PATH).split()
    docs_en = parsexml_list(EN_DOCS_FOLDER_PATH, EN_TAGS, DOC_TAG, DOCNO_TAG, doc_list_en)
    clean_docs_en = clean_data(docs_en, EN_SEPARATORS_RUN1, 0)
    save_to_json(clean_docs_en, EN_CLEAN_DOCS_FILE_PATH)

    # EN train topics
    print("parsing en train topics...")
    topics_train_en = {}
    topics_train_en = parsexml(EN_TRAIN_TOPICS_PATH, topics_train_en, TOPIC_TITLE_TAG, TOPIC_TAG, TOPIC_NUM_TAG)
    clean_topics_en = clean_data(topics_train_en, EN_SEPARATORS_RUN1, 0)
    save_to_json(clean_topics_en, EN_CLEAN_TOPICS_FILE_PATH)

    # EN test topics
    print("parsing en test topics...")
    topics_test_en = {}
    topics_test_en = parsexml(EN_TEST_TOPICS_PATH, topics_test_en, TOPIC_TITLE_TAG, TOPIC_TAG, TOPIC_NUM_TAG)
    clean_topics_en = clean_data(topics_test_en, EN_SEPARATORS_RUN1, 0)
    save_to_json(clean_topics_en, EN_CLEAN_TEST_TOPICS_FILE_PATH)


def parse_full_data_run_2():
    # CZ docs
    print("parsing cz docs...")
    doc_list_cz = read_file(CZ_DOCS_FULL_LIST_PATH).split()
    docs_cz = parsexml_list(CZ_DOCS_FOLDER_PATH, CZ_TAGS, DOC_TAG, DOCNO_TAG, doc_list_cz)
    clean_docs_cz = clean_data(docs_cz, CZ_SEPARATORS_RUN1, 0)
    save_to_json(clean_docs_cz, CZ_CLEAN_DOCS_FILE_PATH)

    # CZ train topics
    print("parsing cz train topics...")
    topics_train_cz = {}
    topics_train_cz = parsexml(CZ_TRAIN_TOPICS_PATH, topics_train_cz, TOPIC_TAGS_RUN2, TOPIC_TAG, TOPIC_NUM_TAG)
    clean_topics_cz = clean_data(topics_train_cz, CZ_SEPARATORS_RUN1, 0)
    save_to_json(clean_topics_cz, CZ_CLEAN_TOPICS_FILE_PATH)

    # CZ test topics
    print("parsing cz test topics...")
    topics_test_cz = {}
    topics_test_cz = parsexml(CZ_TEST_TOPICS_PATH, topics_test_cz, TOPIC_TAGS_RUN2, TOPIC_TAG, TOPIC_NUM_TAG)
    clean_topics_cz = clean_data(topics_test_cz, CZ_SEPARATORS_RUN1, 0)
    save_to_json(clean_topics_cz, CZ_CLEAN_TEST_TOPICS_FILE_PATH)

    # EN docs
    print("parsing en docs...")
    doc_list_en = read_file(EN_DOCS_FULL_LIST_PATH).split()
    docs_en = parsexml_list(EN_DOCS_FOLDER_PATH, EN_TAGS, DOC_TAG, DOCNO_TAG, doc_list_en)
    clean_docs_en = clean_data(docs_en, EN_SEPARATORS_RUN1, 0)
    save_to_json(clean_docs_en, EN_CLEAN_DOCS_FILE_PATH)

    # EN train topics
    print("parsing en train topics...")
    topics_train_en = {}
    topics_train_en = parsexml(EN_TRAIN_TOPICS_PATH, topics_train_en, TOPIC_TAGS_RUN2, TOPIC_TAG, TOPIC_NUM_TAG)
    clean_topics_en = clean_data(topics_train_en, EN_SEPARATORS_RUN1, 0)
    save_to_json(clean_topics_en, EN_CLEAN_TOPICS_FILE_PATH)

    # EN test topics
    print("parsing en test topics...")
    topics_test_en = {}
    topics_test_en = parsexml(EN_TEST_TOPICS_PATH, topics_test_en, TOPIC_TAGS_RUN2, TOPIC_TAG, TOPIC_NUM_TAG)
    clean_topics_en = clean_data(topics_test_en, EN_SEPARATORS_RUN1, 0)
    save_to_json(clean_topics_en, EN_CLEAN_TEST_TOPICS_FILE_PATH)


def parse_reduced_data_run_0():
    # CZ docs
    print("parsing cz docs...")
    doc_list_cz = read_file(CZ_DOCS_REDUCED_LIST_PATH).split()
    docs_cz = parsexml_list(CZ_DOCS_FOLDER_PATH, CZ_TAGS, DOC_TAG, DOCNO_TAG, doc_list_cz)
    clean_docs_cz = clean_data(docs_cz, CZ_SEPARATORS_RUN0, 1)
    save_to_json(clean_docs_cz, CZ_CLEAN_DOCS_FILE_PATH)

    # CZ topics
    print("parsing cz train topics...")
    topics_cz = {}
    topics_cz = parsexml(CZ_TRAIN_TOPICS_PATH, topics_cz, TOPIC_TITLE_TAG, TOPIC_TAG, TOPIC_NUM_TAG)
    clean_topics_cz = clean_data(topics_cz, CZ_SEPARATORS_RUN0, 1)
    save_to_json(clean_topics_cz, CZ_CLEAN_TOPICS_FILE_PATH)

    # CZ test topics
    print("parsing cz test topics...")
    topics_test_cz = {}
    topics_test_cz = parsexml(CZ_TEST_TOPICS_PATH, topics_test_cz, TOPIC_TITLE_TAG, TOPIC_TAG, TOPIC_NUM_TAG)
    clean_topics_cz = clean_data(topics_test_cz, CZ_SEPARATORS_RUN0, 1)
    save_to_json(clean_topics_cz, CZ_CLEAN_TEST_TOPICS_FILE_PATH)

    # EN docs
    print("parsing en docs...")
    doc_list_en = read_file(EN_DOCS_REDUCED_LIST_PATH).split()
    docs_en = parsexml_list(EN_DOCS_FOLDER_PATH, EN_TAGS, DOC_TAG, DOCNO_TAG, doc_list_en)
    clean_docs_en = clean_data(docs_en, EN_SEPARATORS_RUN0, 1)
    save_to_json(clean_docs_en, EN_CLEAN_DOCS_FILE_PATH)

    # EN topics
    print("parsing en train topics...")
    topics_en = {}
    topics_en = parsexml(EN_TRAIN_TOPICS_PATH, topics_en, TOPIC_TITLE_TAG, TOPIC_TAG, TOPIC_NUM_TAG)
    clean_topics_en = clean_data(topics_en, EN_SEPARATORS_RUN0,1)
    save_to_json(clean_topics_en, EN_CLEAN_TOPICS_FILE_PATH)

    # EN test topics
    print("parsing en test topics...")
    topics_test_en = {}
    topics_test_en = parsexml(EN_TEST_TOPICS_PATH, topics_test_en, TOPIC_TITLE_TAG, TOPIC_TAG, TOPIC_NUM_TAG)
    clean_topics_en = clean_data(topics_test_en, EN_SEPARATORS_RUN0, 1)
    save_to_json(clean_topics_en, EN_CLEAN_TEST_TOPICS_FILE_PATH)


def parse_reduced_data_run_1():
    # CZ docs
    print("parsing cz docs...")
    doc_list_cz = read_file(CZ_DOCS_REDUCED_LIST_PATH).split()
    docs_cz = parsexml_list(CZ_DOCS_FOLDER_PATH, CZ_TAGS, DOC_TAG, DOCNO_TAG, doc_list_cz)
    clean_docs_cz = clean_data(docs_cz, CZ_SEPARATORS_RUN1, 0)
    save_to_json(clean_docs_cz, CZ_CLEAN_DOCS_FILE_PATH)

    # CZ train topics
    print("parsing cz train topics...")
    topics_train_cz = {}
    topics_train_cz = parsexml(CZ_TRAIN_TOPICS_PATH, topics_train_cz, TOPIC_TITLE_TAG, TOPIC_TAG, TOPIC_NUM_TAG)
    clean_topics_cz = clean_data(topics_train_cz, CZ_SEPARATORS_RUN1, 0)
    save_to_json(clean_topics_cz, CZ_CLEAN_TOPICS_FILE_PATH)

    # CZ test topics
    print("parsing cz test topics...")
    topics_test_cz = {}
    topics_test_cz = parsexml(CZ_TEST_TOPICS_PATH, topics_test_cz, TOPIC_TITLE_TAG, TOPIC_TAG, TOPIC_NUM_TAG)
    clean_topics_cz = clean_data(topics_test_cz, CZ_SEPARATORS_RUN1, 0)
    save_to_json(clean_topics_cz, CZ_CLEAN_TEST_TOPICS_FILE_PATH)

    # EN docs
    print("parsing en docs...")
    doc_list_en = read_file(EN_DOCS_REDUCED_LIST_PATH).split()
    docs_en = parsexml_list(EN_DOCS_FOLDER_PATH, EN_TAGS, DOC_TAG, DOCNO_TAG, doc_list_en)
    clean_docs_en = clean_data(docs_en, EN_SEPARATORS_RUN1, 0)
    save_to_json(clean_docs_en, EN_CLEAN_DOCS_FILE_PATH)

    # EN train topics
    print("parsing en train topics...")
    topics_train_en = {}
    topics_train_en = parsexml(EN_TRAIN_TOPICS_PATH, topics_train_en, TOPIC_TITLE_TAG, TOPIC_TAG, TOPIC_NUM_TAG)
    clean_topics_en = clean_data(topics_train_en, EN_SEPARATORS_RUN1, 0)
    save_to_json(clean_topics_en, EN_CLEAN_TOPICS_FILE_PATH)

    # EN test topics
    print("parsing en test topics...")
    topics_test_en = {}
    topics_test_en = parsexml(EN_TEST_TOPICS_PATH, topics_test_en, TOPIC_TITLE_TAG, TOPIC_TAG, TOPIC_NUM_TAG)
    clean_topics_en = clean_data(topics_test_en, EN_SEPARATORS_RUN1, 0)
    save_to_json(clean_topics_en, EN_CLEAN_TEST_TOPICS_FILE_PATH)

